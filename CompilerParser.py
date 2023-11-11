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
        ## Generate a parse tree
        class_tree = ParseTree("class", " ")
        class_tree.addChild(self.mustBe("keyword", " class"))
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
        type_values = ["int", "char", "boolean"]
        if self.have('keyword', type_values) is True:
            var_tree.addChild(self.mustBe("keyword", type_values))
        else:
            class_name = self.current().getValue()
            var_tree.addChild(self.mustBe("identifier", class_name))
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
		# type: int, boolean, char, void, class_name #
        type_values = ["int", "char", "boolean", "void"]
        if self.have('keyword', type_values) is True:
            sub_tree.addChild(self.mustBe("keyword", type_values))
        else:
            class_name = self.current().getValue()
            sub_tree.addChild(self.mustBe("identifier", class_name))
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
            pass
        return sub_tree

    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        param_tree = ParseTree("parameterList", " ")
        while self.have("symbol", ")") is False:
            type_values = ["int", "char", "boolean", "void"]
            if self.have('keyword', type_values) is True:
                param_tree.addChild(self.mustBe("keyword", type_values))
            else:
                class_name = self.current().getValue()
                param_tree.addChild(self.mustBe("identifier", class_name))
            param_name = self.current().getValue()
            param_tree.addChild(self.mustBe("identifier", param_name))
            print(param_tree)
            try:
                while self.have("symbol", ",") is True:
                        param_tree.addChild(self.mustBe("symbol", ","))
            except ParseException:
                pass
            try:
                self.current()
            except ParseException as e:
                break
        return param_tree

    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        
        subbody_tree = ParseTree("subroutineBody", " ")
        subbody_tree.addChild(self.mustBe("symbol", "{"))
        try:
          if self.have("keyword", "var"):
              VarDec = self.compileVarDec()
              while VarDec is not None:
                  subbody_tree.addChild(VarDec)
                  VarDec = self.compileVarDec()
        except ParseException as e:
            pass
        subbody_tree.addChild(self.compileStatements())
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
        type_values = ["int", "char", "boolean"]
        if self.have('keyword', type_values) is True:
            var_tree.addChild(self.mustBe("keyword", type_values))
        else:
            class_name = self.current().getValue()
            var_tree.addChild(self.mustBe("identifier", class_name))
        # varName #
        var_name = self.current().getValue()
        var_tree.addChild(self.mustBe("identifier", var_name))
        try:
            while self.have("symbol", ",") is True:
                var_tree.addChild(self.mustBe("symbol", ","))
                var_name = self.current().getValue()
                var_tree.addChild(self.mustBe("identifier", var_name))
        except ParseException:
            print(f'Prase exception compileVarDec: {e}')
        # ; #
        var_tree.addChild(self.mustBe("symbol", ";"))

        return var_tree

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        
        
        """
        statement_tree = ParseTree("statements", " ")
        try:
            if self.have("keyword", "let") is True:
                statement_tree.addChild(self.compileLet())
            elif self.have("keyword", "if") is True:
                    statement_tree.addChild(self.compileIf())
            elif self.have("keyword", "while") is True:
                    statement_tree.addChild(self.compileWhile())
            elif self.have("keyword", "do") is True:
                    statement_tree.addChild(self.compileDo())
            elif self.have("keyword", "return") is True:
                    statement_tree.addChild(self.compileReturn())
        except ParseException as e:
                    print(f'Prase exception compileStatements: {e}')
        return statement_tree

    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        let_tree = ParseTree("letStatement", " ")
        let_tree.addChild(self.mustBe("keyword","let"))
        var_name = self.current().getValue()
        let_tree.addChild(self.mustBe("identifier", var_name))
        try:
             if self.have("symbol", "=") is False:
                  let_tree.addChild(self.mustBe("symbol", "["))
                  let_tree.addChild(self.compileExpression())
                  let_tree.addChild(self.mustBe("symbol", "]"))
        except ParseException as e:
                print(f'Prase exception compileLet: {e}')
        print(let_tree) 
        let_tree.addChild(self.mustBe("symbol", "="))
        let_tree.addChild(self.compileExpression())
        let_tree.addChild(self.mustBe("symbol", ";"))
        return let_tree

    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        if_tree = ParseTree("ifStatement", " ")
        return if_tree

    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        while_tree = ParseTree("whileStatement", " ")
        return while_tree

    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        do_tree = ParseTree("doStatement", " ")
        return do_tree

    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return_tree = ParseTree("returnStatement", " ")
        return return_tree

    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        expression_tree = ParseTree("expression", " ")
        if self.have("keyword", "skip"):
            expression_tree.addChild(self.mustBe("keyword","skip"))
        return expression_tree

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
        return None

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
        
    
        
    tokens.append(Token("keyword", "class"))
    tokens.append(Token("identifier", "MyClass"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("symbol", "}"))
    
    tokens.append(Token("keyword", "class"))
    tokens.append(Token("identifier", "MyClass"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "function"))
    tokens.append(Token("keyword", "int"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", "("))
    tokens.append(Token("symbol", ")"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "let"))
    tokens.append(Token("identifier", "varName"))
    tokens.append(Token("symbol", "="))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    tokens.append(Token("symbol", "}"))
    
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "let"))
    tokens.append(Token("identifier", "varName"))
    tokens.append(Token("symbol", "["))
    tokens.append(Token("stringConstant", '"hello"'))
    tokens.append(Token("symbol", "]"))
    tokens.append(Token("symbol", "="))
    tokens.append(Token("stringConstant", '"hello"'))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    
    tokens.append(Token("keyword", "int"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", ","))
    tokens.append(Token("keyword", "char"))
    tokens.append(Token("identifier", "b"))
    tokens.append(Token("symbol", ","))
    tokens.append(Token("keyword", "boolean"))
    tokens.append(Token("identifier", "c"))
    tokens.append(Token("symbol", ","))
    tokens.append(Token("identifier", "Test"))
    tokens.append(Token("identifier", "d"))
        
    """
    tokens = []
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("keyword", "let"))
    tokens.append(Token("identifier", "a"))
    tokens.append(Token("symbol", "="))
    tokens.append(Token("keyword", "skip"))
    tokens.append(Token("symbol", ";"))
    tokens.append(Token("symbol", "}"))
    
    parser = CompilerParser(tokens)
    try:
        result = parser.compileSubroutineBody()
        print(result)
    except ParseException:
        print("Error Parsing!")
