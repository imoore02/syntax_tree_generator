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
        subroutine_values = ["constructor", "function", "method"]
        try:
            while self.tokens:
                if self.have("keyword", subroutine_values):
                    program_tree.addChild(self.compileSubroutine())
        except ParseException:
            pass
        return program_tree

    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        ## Generate a parse tree
        class_tree = ParseTree("class", " ")
        class_tree.addChild(self.mustBe("keyword", " class"))
        global class_name
        class_name = self.current().getValue()
        class_tree.addChild(self.mustBe("identifier", class_name))
        # { #
        class_tree.addChild(self.mustBe("symbol", "{"))
        try:
          VarDec = self.compileClassVarDec()
          while VarDec is not None:
            class_tree.addChild(VarDec)
            VarDec = self.compileClassVarDec()
        except ParseException:
            pass
        try:
            Subroutine = self.compileSubroutine()
            while Subroutine is not None:
                class_tree.addChild(Subroutine)
                Subroutine = self.compileSubroutine()
        except ParseException:
            pass   
        class_tree.addChild(self.mustBe("symbol", "}"))
        return class_tree

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        expected_values = ["static", "field"]
        # Generate parse tree
        var_tree = ParseTree("classVarDec", " ")
        # static|field #
        var_tree.addChild(self.mustBe("keyword", expected_values))
        # type: int, boolean, char, void, class_name #
        type_values = ["int", "char", "boolean", class_name]
        var_tree.addChild(self.mustBe("keyword", type_values))
        # varName #
        var_name = self.current().getValue()
        var_tree.addChild(self.mustBe("identifier", var_name))
        try:
            while self.have("symbol", ","):
                var_tree.addChild(self.mustBe("symbol", ","))
                var_name = self.current().getValue()
                var_tree.addChild(self.mustBe("identifier", var_name))
        except ParseException:
            pass 
        # ; #
        var_tree.addChild(self.mustBe("symbol", ";"))

        return var_tree

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        # Check that a subroutine is present
        subroutine_values = ["method", "function", "constructor"]
        # Generate a parse tree for the subroutine
        sub_tree = ParseTree("subroutine", " ")
        # constructor|function|method #
        sub_tree.addChild(self.mustBe("keyword", subroutine_values))
        print(sub_tree)
        type_values = ["int", "char", "boolean", "void", class_name]
        lst = ["keyword", "identifier"]
        sub_tree.addChild(self.mustBe(lst, type_values))
        # className #
        subroutine_name = self.current().getValue()
        sub_tree.addChild(self.mustBe("identifier", subroutine_name))
        # ( #
        sub_tree.addChild(self.mustBe("symbol", "("))
        Params = self.compileParameterList()
        sub_tree.addChild(Params)
        sub_tree.addChild(self.mustBe("symbol", ")"))
        try:
             SubroutineBody = self.compileSubroutineBody()
             while SubroutineBody is not None:
                 sub_tree.addChild(SubroutineBody)
                 SubroutineBody = self.compileSubroutineBody()
        except ParseException as e:
            print(f"ParseException in subrlutine(body): {e}")
            
        return sub_tree

    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        param_tree = ParseTree("parameterList", " ")
        try:
            while self.have('symbol', ')') is False:
                 param_name = self.current().getValue()
                 param_tree.addChild(self.mustBe('keyword', param_name))
                 param_name = self.current().getValue()
                 param_tree.addChild(self.mustBe("identifier", param_name))
                 try:
                      while self.have("symbol", ",") is True:
                              param_tree.addChild(self.mustBe("symbol", ","))
                              param_name = self.current().getValue()
                              param_tree.addChild(self.mustBe("identifier", param_name))
                 except ParseException:
                     pass
        except ParseException:
            pass
                
        return param_tree

    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        
        subbody_tree = ParseTree("subroutineBody", " ")
        subbody_tree.addChild(self.mustBe("symbol", "{"))
        try:
          VarDec = self.compileVarDec()
          while VarDec is not None:
            subbody_tree.addChild(VarDec)
            VarDec = self.compileVarDec()
        except ParseException:
            pass
        subbody_tree.addChild(self.mustBe("symbol", "}"))

        return subbody_tree

    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        # Generate parse tree
        var_tree = ParseTree("varDec", " ")
        # static|field #
        var_tree.addChild(self.mustBe("keyword", "var"))
        # type: int, boolean, char, void, class_name #
        type_values = ["int", "char", "boolean", class_name]
        var_tree.addChild(self.mustBe("keyword", type_values))
        # varName #
        var_name = self.current().getValue()
        var_tree.addChild(self.mustBe("identifier", var_name))
        try:
            while self.have("symbol", ",") is True:
                var_tree.addChild(self.mustBe("symbol", ","))
                var_name = self.current().getValue()
                var_tree.addChild(self.mustBe("identifier", var_name))
        except ParseException:
            pass
        # ; #
        var_tree.addChild(self.mustBe("symbol", ";"))

        return var_tree

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
        raise ParseException(
                f"Expected type: {expectedType} and expected value: {expectedValue}. Detected type: {self.current().getType()} and detected value: {self.current().getValue()}"
            )

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


if __name__ == "__main__":
    """
    Tokens for:
        class MyClass {

        }
    """
    tokens = []
    tokens.append(Token("keyword", "class"))
    tokens.append(Token("identifier", "Test"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "constructor"))
    tokens.append(Token("keyword", "Test"))
    tokens.append(Token("identifier", "new"))
    tokens.append(Token("symbol", "("))
    tokens.append(Token("symbol", ")"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("symbol", "}"))
    tokens.append(Token("symbol", "}"))
    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
