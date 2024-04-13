// Vulnerable code
var obj = {};
var data = JSON.parse('{"__proto__": {"isAdmin": true}}');
Object.assign(obj, data);

// Check if the object has isAdmin property
if (obj.isAdmin) {
    console.log("User is admin!");
} else {
    console.log("User is not admin!");
}
