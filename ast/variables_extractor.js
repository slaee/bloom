const fs = require('fs');
const {Parser} = require("acorn")

const sourceType = process.argv[2]

const src = fs.readFileSync(process.argv[3], 'utf8')

let tree;
try {
    tree = Parser.parse(src, {'locations': true, 'sourceType': sourceType,
                                'ecmaVersion': 'latest'})
} catch (e) {
    process.stderr.write(e.message)
    process.exit(1)
}


// process.stdout.write(JSON.stringify(tree))

const variables = []

function walk(node, parent) {
    if (node.type === 'VariableDeclaration') {
        node.declarations.forEach(decl => {
            if (decl.id.type === 'Identifier') {
                variables.push(decl.id.name)
            } else {
                walk(decl.id, node) // should include the variables from destructuring 'ObjectPattern'
            }
        })
    }

    if (node.type === 'ObjectPattern') {
        node.properties.forEach(prop => {
            variables.push(prop.key.name)
        })
    }

    for (let key in node) {
        if (node[key] && typeof node[key] === 'object') {
            walk(node[key], node)
        }
    }
}

walk(tree)

// remove any duplicates
const uniqueVariables = new Set(variables)
// remove all nulls
uniqueVariables.delete(null)
uniqueVariables.delete('')

let i = 0
uniqueVariables.forEach(v => {
    if (i === uniqueVariables.size - 1) {
        process.stdout.write(v)
        return
    }
    process.stdout.write(v + ',')
    i++
})