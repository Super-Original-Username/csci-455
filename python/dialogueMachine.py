import sys
import re   # I decided to go with regexes for building parts of the parser, just to allow a little more line flexibility

'''
multiple regexes are designed to do a sort of pseudo (maybe full? I'm a little rusty on the old design patterns) visitor pattern, partially 'tokenizing'
line segments so the tree generation can hop between functions and do different operations for each type of item
'''
u_reg = r'^u[0-9]*' # this allows for as many response path children as you could possibly want. 
prop_reg = r'&p'    # simple regex for matching the proposal
comm_reg = r'#.*'   # this regex is just to strip comments out of the input file
def_reg = r'~'      # regex for definitions
multiChoice_reg = r'\(\[([a-z\s"]*,?)+\]\)'
filename_reg = r'.*\.tangoChat' # This is used as part of a couple of checks that the user file input will work

'''
    Note:
    When writing a tangoChat file, keep in mind that this program generates its list of
    potential responses for each dialog node by checking the first character after the
    colon in each line. MAKE SURE THAT THERE MU
'''

class decision_node:
    def __init__(self,type = None, level = 0, parent_level = -1,parent = None, resp = '', inputs = []):
        self.type = type
        self.level = level
        self.parent_level = parent_level # having this allows for a simple form of scoping, using the parent node as a symbol table of sorts
        self.parent = parent
        self.resp = resp
        self.inputs = inputs
        self.children = []

    def add_child(self, in_node):
        self.children.append(in_node)

    def set_inputs(self, in_inputs):
        in_inputs = in_inputs.split(',')
        for item in in_inputs:
            item = item.replace('"','')
            item = item.replace("'",'')
        self.inputs = in_inputs

    def __str__(self):
        out_string = "type: "+str(self.type)+"\nparent level: "+ str(self.parent_level)+"\nlevel: "+str(self.level)+"\ninputs: " + ', '.join(item for item in self.inputs)+"\nresponse: "+str(self.resp)
        #inputs_string = ', '.join(item for item in self.inputs)
        #out_string += inputs_string
        out_string += '\n'
        print(out_string)




class decision_tree:
    def __init__(self,in_filename):
        self.root = decision_node()
        self.root_generated = False
        self.cur_parent = self.root
        self.prev_node = self.root
        try:
            convo_file = open(in_filename) 
        except expression as identifier:
            print("--{Yeah, it sure doesn't look like this file exists, chief}--")
            print(identifier)
            return

        convo_string = convo_file.readlines()
        tokenized_convo = []
        for line in convo_string:
            line = line.lower() # casts the entire row into lowercase to remove any need for case sensitivity
            line = line.strip() # cuts off any newlines from the current line
            line = line.split(':') # splits a line from type:inputs:response into a list of [type, inputs, response]
            for segment in line: 
                segment = segment.strip(" ") # removes any extra spaces surrounding the current line segment
            tokenized_convo.append(line)
        self.process_file(tokenized_convo)


    def process_file(self, input_string):
        for line in input_string:
            if not self.root_generated:
                if not re.match(prop_reg, line[0]):
                    print("--{This isn't a proposal line, checking next}--")
                else:
                    print("--{Proposal line found, beginning tree generation}--")
                    self.generate_root(line)
            elif re.match(u_reg,line[0]):
                # logic to place dialogue options in the correct place in the tree
                if int(line[0][1]) == self.prev_node.level-1:
                    self.cur_parent = self.cur_parent.parent
                elif int(line[0][1]) == self.prev_node.level+1:
                    self.cur_parent = self.prev_node
                self.process_u_node(line,self.cur_parent)



    '''When the above function comes across any 'level' of 'u', it hops into this function to begin adding a new 
        node to the conversation tree'''
    def process_u_node(self,line,parent_node):
        inputs = []
        resp = line[2]
        level = int(line[0][1])
        temp_inputs = line[1]
        if re.match(multiChoice_reg,line[1]):
            inputs = self.process_multiChoice(line[1])
        else:
            temp_inputs = re.sub(r'[\(\)]','',temp_inputs) # This is just for a single possible input for the line
            temp_inputs = temp_inputs.strip()
            temp_inputs = temp_inputs.strip(" ")
            temp_inputs = temp_inputs.strip('"')
            inputs.append(temp_inputs)
        new_option = decision_node(type='u',level = level,parent_level=parent_node.level,parent=parent_node,resp=resp,inputs=inputs)
        self.prev_node = new_option
        parent_node.add_child(new_option)


    '''This returns a list of possible user replies for the node. Could I have done this in the regular old
        "process_u_node" function? Probably, but I had already written that nasty regex up top, so I didn't want it to go to waste'''
    def process_multiChoice(self, seg):
        multi = str(seg)
        multi = re.sub(r'[\(\[\)\]]','',multi) # removes the surrounding ([]) from the segment of the line containing the soon-to-be list
        multi = multi.split(',') # converts the line into a list
        modified_multi = []
        for item in multi:
            item = item.strip() # removes newlines
            item = item.strip(" ") # removes spaces
            item = item.strip('"') # removes quotations
            modified_multi.append(item)
        return modified_multi
        

    '''The root node is built separately, because of course it is'''
    def generate_root(self,line):
        self.root.type = "proposal"
        self.root.resp = line[1]
        self.root_generated = True

    '''This begins the conversation. It is called "other" because there were other methods that 
        I tried before doing this one, and then I was too lazy to change the name after I was done'''
    def other_converse(self,cur):
        print(cur.resp)
        if len(cur.children) != 0:
            reply = input()
            for child in cur.children:
                for possible_reply in child.inputs:
                    if reply == possible_reply:
                        self.other_converse(child)
                        return
        return



    def traverse(self,par):
        par.__str__()
        for child in par.children:
            self.traverse(child)

    def test_root(self):
        self.root.__str__()


        
# used to check if there was an input for the filename
def fileAvailableCheck():
    if sys.argv[1] is None:
        return False
    else:
        return True

def main():
    convo_tree = ''
    if not fileAvailableCheck():
        return
    else:
        toOpen = sys.argv[1]
        if re.match(filename_reg, toOpen):
            convo_tree = decision_tree(toOpen)
            #convo_tree.test_root()
            #convo_tree.traverse(convo_tree.root)
            convo_tree.other_converse(convo_tree.root)
            print("--{Dialogue complete}--")
        else:
            print("Your input file does not follow the requirement: *.tangoChat\nPlease try again with the correct filetype")

    

if __name__ == "__main__":
    main()

