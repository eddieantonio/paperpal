/*!
 * Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * This is a "runtime" for Python to talk to Zotero. It provides a library of
 * common tasks, and protocol for communicating to Python via JSON. Note that
 * the following immediately-invoked function expression (IIFE) **MUST** be
 * the last expression in the file!
 *
 * The API is this:
 *
 * Python INTENTIONALLY injects code into this snippet, passing an "action" as
 * a string, and any additional arguments through a JSON called "options".
 * This script executes in Zotero's context. The goal of the following
 * function is to return to Python a JSON expression of:
 *
 *      ['ok', result]
 *
 * or
 *
 *      ['error', reason]
 *
 * Originally derived from Jason Friedman's work:
 * http://www.curiousjason.com/zoterotobibtex.html
 */
(function (actionName, options) {
    var BIBTEX_ID = '9cb70025-a888-4a29-a210-93ec52da40d4';

    var bibtextId = '9cb70025-a888-4a29-a210-93ec52da40d4';
    var betterBibTexId = 'f895aa0d-f28e-47fe-b247-2ea77c6ed583';

    var Zotero = Components.classes['@zotero.org/Zotero;1']
        .getService(Components.interfaces.nsISupports)
        .wrappedJSObject;

    var actions = {
        /**
         * Exports Bibliography in the requested format to the given filename.
         *
         * Option parameters:
         *
         *  collection: name of the collection to export
         *  filename:   filename of file to save
         *  translator: [optional] ID of translator; uses BibTex by default.
         */
        exportBibliography: withNamedCollection(function (collection) {
            var translator = new Zotero.Translate.Export();
            translator.setTranslator(options.translator || betterBibTexId);
            translator.setLocation(openFile(options.filename));
            translator.setCollection(collection);

            translator.translate();

            return ['ok', options.filename];
        }),

        /**
         * Lists item in the bibliography in the following format:
         *
         * [{
         *      title: _,
         *      authors: _,
         *      year: _,
         *      citeKey: _,
         *      pdfFilename: _
         *  }]
         *
         * Option parameters:
         *
         *  collection: name of the collection to list
         */
        list: withNamedCollection(function (collection) {
            return ['error', 'not_implemented'];
        })
    };

    /* Find the action and execute it. */
    if (!actions[actionName]) {
        return ['error', ['unknown_action', actionName]];
    }
    return actions[actionName]();

    /* === Library === */

    function getNamedCollection(name) {
        var collections = Zotero.getCollections();
        var collection = collections.filter(function (c) {
            return c.name === name;
        })[0];

        /* Return null if collection does not exist. */
        return !!collection ? collection : null;
    }

    function openFile(filename) {
        var file = Components.classes["@mozilla.org/file/local;1"]
            .createInstance(Components.interfaces.nsILocalFile);

        file.initWithPath(filename);

        return file;
    }

    function withNamedCollection(callback) {
        return function () {
            var collection = getNamedCollection(options.collection);
            if (collection === null) {
                return ['error', ['unknown_collection', options.collection]];
            }

            return callback(collection)
        };
    }
}(/* %(close_comment)s %(action)s, %(options)s %(open_comment)s */));
/*globals Components */
/*eslint no-define-before-use: false*/
