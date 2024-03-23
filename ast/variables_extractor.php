<?php
require_once __DIR__ . '/vendor/autoload.php';

use PhpParser\{Error, NodeDumper, ParserFactory};

$filename = $argv[1];

if (!file_exists($filename)) {
    echo "File does not exist: $filename\n";
    exit(1);
}

$code = file_get_contents($filename);

$parser = (new ParserFactory())->createForNewestSupportedVersion();

function walk($node, &$variables, $code) {
    // Handle conditions
    if ($node instanceof PhpParser\Node\Expr\ArrayDimFetch) {
        if ($node->var instanceof PhpParser\Node\Expr\Variable) {
            $variables[] = '$' . $node->var->name . "['" . $node->dim->value . "']";
        }
    }

    if ($node instanceof PhpParser\Node\Expr\Variable) {
        $variables[] = '$' . $node->name;
    }

    // Handle function parameters
    if ($node instanceof PhpParser\Node\Param) {
        $variables[] = '$' . $node->var->name;
    }

    // Handle conditions
    if ($node instanceof PhpParser\Node\Expr\BinaryOp\Equal
        || $node instanceof PhpParser\Node\Expr\BinaryOp\Identical
        || $node instanceof PhpParser\Node\Expr\BinaryOp\NotEqual
        || $node instanceof PhpParser\Node\Expr\BinaryOp\NotIdentical
        || $node instanceof PhpParser\Node\Expr\BinaryOp\Greater
        || $node instanceof PhpParser\Node\Expr\BinaryOp\GreaterOrEqual
        || $node instanceof PhpParser\Node\Expr\BinaryOp\Smaller
        || $node instanceof PhpParser\Node\Expr\BinaryOp\SmallerOrEqual
        || $node instanceof PhpParser\Node\Expr\BinaryOp\LogicalAnd
        || $node instanceof PhpParser\Node\Expr\BinaryOp\LogicalOr
    ) {
        walk($node->left, $variables, $code);
        walk($node->right, $variables, $code);
    }

    // Handle isset constructs
    if ($node instanceof PhpParser\Node\Expr\Isset_) {
        foreach ($node->vars as $var) {
            if ($var instanceof PhpParser\Node\Expr\Variable) {
                $variables[] = '$' . $var->name;
            } elseif ($var instanceof PhpParser\Node\Expr\ArrayDimFetch
                && $var->var instanceof PhpParser\Node\Expr\Variable) {
                $variableName = '$' . $var->var->name;

                // Handle the array index itself if it's a variable
                if ($var->dim instanceof PhpParser\Node\Expr\Variable) {
                    $variableName .= "['$" . $var->dim->name . "']";
                } elseif ($var->dim instanceof PhpParser\Node\Scalar\String_
                    || $var->dim instanceof PhpParser\Node\Scalar\LNumber) {
                    $variableName .= "['" . $var->dim->value . "']";
                }

                $variables[] = $variableName;
            } elseif ($var instanceof PhpParser\Node\Expr\Isset_) {
                // Handle nested isset constructs
                foreach ($var->vars as $nestedVar) {
                    walk($nestedVar, $variables, $code);
                }
            }
        }
    }

    // Handle variables in conditions
    if ($node instanceof PhpParser\Node\Expr\Variable) {
        $variables[] = '$' . $node->name;
    }

    if ($node instanceof PhpParser\Node\Stmt\If_
        || $node instanceof PhpParser\Node\Stmt\ElseIf_
        || $node instanceof PhpParser\Node\Stmt\Else_
    ) {
        // Handle condition expression
        if (property_exists($node, 'cond') && $node->cond instanceof PhpParser\Node) {
            walk($node->cond, $variables, $code);
        }

        // Handle statements inside the if statement
        foreach ($node->stmts as $stmt) {
            if ($stmt instanceof PhpParser\Node) {
                walk($stmt, $variables, $code);
            }
        }

        // Handle elseif and else conditions
        if ($node instanceof PhpParser\Node\Stmt\ElseIf_) {
            foreach ($node->elseifs as $elseif) {
                if ($elseif->cond instanceof PhpParser\Node) {
                    walk($elseif->cond, $variables, $code);
                }

                foreach ($elseif->stmts as $stmt) {
                    if ($stmt instanceof PhpParser\Node) {
                        walk($stmt, $variables, $code);
                    }
                }
            }
        } elseif ($node instanceof PhpParser\Node\Stmt\Else_) {
            foreach ($node->stmts as $stmt) {
                if ($stmt instanceof PhpParser\Node) {
                    walk($stmt, $variables, $code);
                }
            }
        }
    }

    // Handle other statements
    foreach ($node->getSubNodeNames() as $subNodeName) {
        $subNode = $node->$subNodeName;
        if ($subNode instanceof PhpParser\Node) {
            walk($subNode, $variables, $code);
        }
    }
}

// Handle functions
function handleFunction($node, &$variables, $code) {
    // Handle function parameters
    foreach ($node->params as $param) {
        if ($param instanceof PhpParser\Node\Param) {
            $variables[] = '$'.$param->var->name;
        }
    }

    // Handle function body
    foreach ($node->stmts as $stmt) {
        if ($stmt instanceof PhpParser\Node) {
            walk($stmt, $variables, $code);
        }
    }
}

try {
    $stmts = $parser->parse($code);
    $variables = array();

    foreach ($stmts as $stmt) {
        if ($stmt instanceof PhpParser\Node\Stmt\Function_) {
            // Handle functions separately
            handleFunction($stmt, $variables, $code);
        } else {
            walk($stmt, $variables, $code);
        }
    }

    // Remove all duplicates
    $variables = array_unique($variables);

    // Remove all $_GET, $_POST, $_SERVER, $_COOKIE, $_SESSION, $_FILES, $_ENV with no array shim '[]'
    $variables = array_filter($variables, function($var) {
        if (preg_match('/\$_(GET|POST|SERVER|COOKIE|SESSION|FILES|ENV)\b/', $var)
        && strpos($var, '[') === false) {
            return false;
        }

        return true;
    });

    // Sort the variables based on their appearance in the code
    usort($variables, function($a, $b) use ($code) {
        return strpos($code, $a) <=> strpos($code, $b);
    });

    for ($i = 0; $i < count($variables); $i++) {
        echo $variables[$i];

        if ($i < count($variables) - 1) {
            echo ',';
        }
    }

} catch (PhpParser\Error $e) {
    echo 'Parse Error: ', $e->getMessage();
    exit(1);
}
?>
