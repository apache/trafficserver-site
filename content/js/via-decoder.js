/*
 * Decoder for Apache Traffic Server Via header codes.
 *
 * Shared between the website (loaded as a plain script, exposed as
 * window.ViaDecoder) and the pytest suite in tests/ (loaded with require()
 * under node).
 *
 * The parser is tag-driven, mirroring src/traffic_via/traffic_via.cc in
 * apache/trafficserver: a lowercase letter selects a field, the uppercase
 * letters and spaces that follow are that field's values, and ':' or ';'
 * separates the standard section from the detail section. This handles every
 * via variant regardless of length: the current 22-character form, the
 * pre-8.0 24-character form with the ICP tag, short response forms, vias
 * missing the leading client pair, and vias whose trailing spaces were
 * stripped in copy/paste (a missing trailing value decodes as ' ').
 */
(function (global) {
  "use strict";

  // Fields before the ':' separator.
  var STANDARD_FIELDS = {
    u: [
      {
        title: "Request headers received from client",
        values: {
          C: "cookie",
          E: "error in request",
          S: "simple request (not conditional)",
          N: "no-cache",
          I: "If-Modified-Since (IMS)",
          " ": "unknown",
        },
      },
    ],
    c: [
      {
        title: "Result of Traffic Server cache lookup for URL",
        values: {
          A: 'in cache, not acceptable (a cache "MISS")',
          H: 'in cache, fresh (a cache "HIT")',
          S: 'in cache, stale (a cache "MISS")',
          R: 'in cache, fresh RAM hit (a cache "HIT")',
          W: 'in cache, fresh Read While Write (a cache "HIT")',
          M: 'miss (a cache "MISS")',
          " ": "no cache lookup",
        },
      },
    ],
    s: [
      {
        title: "Response information received from origin server",
        values: {
          E: "error in response",
          S: "connection opened successfully",
          N: "not-modified",
          " ": "no server connection needed",
        },
      },
    ],
    f: [
      {
        title: "Result of document write-to-cache",
        values: {
          U: "updated old cache copy",
          D: "cached copy deleted",
          W: "written into cache (new copy)",
          " ": "no cache write performed",
        },
      },
    ],
    p: [
      {
        title: "Proxy operation result",
        values: {
          R: "origin server revalidated",
          S: "served or connection opened successfully",
          N: "not-modified",
          " ": "unknown",
        },
      },
    ],
    e: [
      {
        title: "Error codes (if any)",
        values: {
          A: "authorization failure",
          H: "header syntax unacceptable",
          C: "connection to server failed",
          T: "connection timed out",
          S: "server related error",
          D: "dns failure",
          N: "no error",
          F: "request forbidden",
          R: "cache read error",
          M: "moved temporarily",
          L: "loop detected",
          " ": "unknown",
        },
      },
    ],
  };

  // Fields after the ':' (or ';') separator. The 'c' tag carries two values:
  // cache type followed by cache lookup result.
  var DETAIL_FIELDS = {
    t: [
      {
        title: "Tunnel info",
        values: {
          " ": "no tunneling",
          U: "tunneling because of url (url suggests dynamic content)",
          M: "tunneling due to a method (e.g. CONNECT)",
          O: "tunneling because cache is turned off",
          F: "tunneling due to a header field (such as presence of If-Range header)",
          N: "tunneling due to no forward",
          A: "tunnel authorization",
        },
      },
    ],
    c: [
      {
        title: "Cache Type",
        values: {
          C: "cache",
          L: "cluster (not used)",
          P: "parent",
          S: "server",
          I: "ICP (legacy)",
          " ": "unknown",
        },
      },
      {
        title: "Cache Lookup Result",
        values: {
          C: "cache hit, but config forces revalidate",
          I: "conditional miss (client sent conditional, fresh in cache, returned 412)",
          " ": "cache miss or no cache lookup",
          U: "cache hit, but client forces revalidate (e.g. Pragma: no-cache)",
          D: "cache hit, but method forces revalidate (e.g. ftp, not anonymous)",
          M: "cache miss (url not in cache)",
          N: "conditional hit (client sent conditional, doc fresh in cache, returned 304)",
          H: "cache hit",
          S: "cache hit, but expired",
          K: "cookie miss",
        },
      },
    ],
    p: [
      {
        title: "Parent proxy connection status",
        values: {
          " ": "no parent proxy or unknown",
          S: "connection opened successfully",
          F: "connection open failed",
        },
      },
    ],
    s: [
      {
        title: "Origin server connection status",
        values: {
          " ": "no server connection needed",
          S: "connection opened successfully",
          F: "connection open failed",
        },
      },
    ],
  };

  // Pull the via code out of arbitrary input: a bare code, a code in square
  // brackets, or a whole Via header line such as
  // "HTTP/1.1 host (ApacheTrafficServer/10.0.0 [uScMsSfWpSeN:t cCMpSs ])".
  // Other bracketed parts of a header (the process UUID, the protocol stack)
  // contain digits or punctuation, so they never match.
  function extractViaCode(input) {
    var bracketed = input.match(/\[([A-Za-z:; ]+)\]/);
    if (bracketed) {
      return bracketed[1];
    }
    var runs = input.match(/[A-Za-z:; ]+/g);
    if (!runs) {
      return null;
    }
    var longest = "";
    for (var i = 0; i < runs.length; i++) {
      if (runs[i].length > longest.length) {
        longest = runs[i];
      }
    }
    // Leading whitespace is noise; trailing spaces are significant values.
    return longest.replace(/^\s+/, "") || null;
  }

  function decodeVia(input) {
    var code = extractViaCode(String(input == null ? "" : input));
    var fields = [];
    var explicit = 0;

    if (code) {
      var detail = false;
      var pending = []; // field definitions awaiting their value characters

      var emit = function (def, section, ch, padded) {
        var known = Object.prototype.hasOwnProperty.call(def.values, ch);
        var f = {
          section: section,
          title: def.title,
          code: ch,
          description: known ? def.values[ch] : "invalid value '" + ch + "'",
        };
        if (!known) {
          f.unknown = true;
        }
        if (padded) {
          f.padded = true;
        } else {
          explicit++;
        }
        fields.push(f);
      };

      var section = function () {
        return detail ? "operational" : "proxy";
      };

      // A tag with no remaining values means trailing spaces were stripped
      // from the input; decode the missing values as ' '.
      var padPending = function () {
        while (pending.length) {
          emit(pending.shift(), section(), " ", true);
        }
      };

      for (var i = 0; i < code.length; i++) {
        var ch = code.charAt(i);
        if (ch === ":" || ch === ";") {
          padPending();
          detail = true;
        } else if (ch >= "a" && ch <= "z") {
          padPending();
          var defs = (detail ? DETAIL_FIELDS : STANDARD_FIELDS)[ch];
          // Unknown tags (e.g. the legacy 'i' ICP tag) are skipped; their
          // value characters fall through with nothing pending.
          pending = defs ? defs.slice() : [];
        } else if (pending.length) {
          emit(pending.shift(), section(), ch, false);
        }
      }
      padPending();
    }

    if (explicit === 0) {
      return {
        ok: false,
        error:
          "No valid Traffic Server via codes found. Expected something like " +
          '"uScMsSfWpSeN:t cCMp sS" or a full Via header containing it.',
        via: code || "",
        fields: [],
      };
    }
    return { ok: true, error: null, via: code, fields: fields };
  }

  var api = { decodeVia: decodeVia };
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    global.ViaDecoder = api;
  }
})(this);
