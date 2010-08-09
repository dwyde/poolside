function(doc, req) {
    // !json templates.test.nb
    // !code vendor/couchapp/lib/mustache.js

    return Mustache.to_html(templates.test.nb, {
        doc : doc,
        docid : toJSON((doc && doc._id) || null),
        fruits: doc.fruits,
    });

}
