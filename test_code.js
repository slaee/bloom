// Prototype Pollution
function polluteObject(obj, key, value) {
    obj[key] = value;
  }
  
  // Original object
  let originalObject = {};
  
  // Pollution
  polluteObject(originalObject, "__proto__", { isAdmin: true });
  
  // XSS
  let userInput = "<script>alert('XSS Attack!');</script>";
  
  // Displaying the user input in HTML
  document.getElementById("output").innerHTML = userInput;
  