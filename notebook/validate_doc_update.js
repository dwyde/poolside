function(newDoc, oldDoc, userCtx) {
  /* Admins can edit anything. */  
  if (userCtx.roles.indexOf('_admin') !== -1) {
    return;
  }
  
  if (userCtx.name === null) {
    throw({unauthorized: 'Log in before updating a document.'});
  }
  
  if (newDoc._deleted === true) {
    if (oldDoc.writers.indexOf(userCtx.name) !== -1) {
      return;
    }
    else {
      throw({unauthorized: 'You aren\'t authorized to delete this document.'});
    }
  }
  
  var newType = newDoc.type;
  if (newType == 'cell' || newType == 'worksheet') {
    if (!newDoc.writers) {
      throw({forbidden: 'The "writers" field is required.'});
    }
    if (newDoc.writers.indexOf(userCtx.name) == -1) {
      throw({forbidden: 'The "writers" field must include your user.'});
    }
    if (oldDoc && toJSON(oldDoc.writers) != toJSON(newDoc.writers)) {
      throw({forbidden: 'You can\'t modify the "writers" field.'});
    }
  }
  else {
    throw({forbidden: 'Bad document type.'});
  }
  
    
    
}