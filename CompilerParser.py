from ParseTree import *


class CompilerParser:
    def __init__(self, tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.current_token_index = 0

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        # are there tokens to parse? (does the token string exist?)
        if not self.tokens:
            raise ParseException("No tokens to parse")
        program_tree = self.compileClass()
        return program_tree

    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        if not self.have("keyword", "class"):
            raise ParseException("The program does not begin with a class")
        
        ## Generate a parse tree
        class_tree = ParseTree("class", " ")
        class_tree.addChild(self.mustBe("keyword", " class"))
        # className #
        class_name = self.current().getValue()
        class_tree.addChild(self.mustBe("identifier", class_name))
        # { #
        class_tree.addChild(self.mustBe("symbol", "{"))
        print(class_tree)
        try:
          VarDec = self.compileClassVarDec(class_name)
          while VarDec is not None:
            class_tree.addChild(VarDec)
            VarDec = self.compileClassVarDec(class_name)
        except ParseException as e:
         print(f"ParseException: {e}")
        class_tree.addChild(self.mustBe("symbol", "}"))
        return class_tree

    def compileClassVarDec(self, class_name):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        expected_values = ["static", "field"]
        if not self.have("keyword", expected_values):
            raise ParseException("A non class variable declaration was detected")
        # Generate parse tree
        var_tree = ParseTree("classVarDec", " ")
        # static|field #
        var_tree.addChild(self.mustBe("keyword", expected_values))
        # type: int, bool etc #
        type_values = ["int", "char", "boolean", class_name]
        var_tree.addChild(self.mustBe("keyword", type_values))
        # varName #
        var_name = self.current().getValue()
        var_tree.addChild(self.mustBe("identifier", var_name))
        # ; #
        var_tree.addChild(self.mustBe("symbol", ";"))

        return var_tree

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        return None

    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        return None

    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        return None

    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        return None

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        return None

    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        return None

    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        return None

    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        return None

    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        return None

    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return None

    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        return None

    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None

    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None

    def next(self):
        """
        Advance to the next token
        """
        self.current_token_index += 1
        return

    def current(self):
        """
        Return the current token
        @return the token
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        else:
            raise ParseException("No more tokens available")

    def have(self, expectedType, expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        current_token = self.current()
        if (
            current_token.getType() == expectedType
            and current_token.getValue() == expectedValue
        ):
            return True
        elif (
            current_token.getType() in expectedType
            and current_token.getValue() in expectedValue
        ):
            return True
        raise ParseException("Current token does not match type or value")
        return False

    def mustBe(self, expectedType, expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        current_token = self.current()
        if self.have(expectedType, expectedValue) == True:
            self.next()
            return current_token
        else:
            raise ParseException(
                f"Expected type: {expectedType} and expected value: {expectedValue}. Detected type: {self.current().getType()} and detected value: {self.current().getValue()}"
            )
        return None


if __name__ == "__main__":
    """
    Tokens for:
        class MyClass {

        }
    """
    tokens = []
    tokens.append(Token("keyword", "class"))
    tokens.append(Token("identifier", "MyClass"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "static"))
    tokens.append(Token("keyword", "int"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("keyword", "field"))
    tokens.append(Token("keyword", "boolean"))
    tokens.append(Token("identifier", "myName"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
