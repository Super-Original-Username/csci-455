'''This program uses .tangoChat files to generate dynamically-sized dialogue trees. It has a few limitations, as noted below, though can pretty much handle anything
    you throw at it, so long as they fall within the guidelines of the assigment
 '''

import sys
import re   # I decided to go with regexes for building parts of the parser, just to allow a little more line flexibility
import random

'''
multiple regexes are designed to do a sort of pseudo (maybe full? I'm a little rusty on the old design patterns) visitor pattern, partially 'tokenizing'
line segments so the tree generation can hop between functions and do different operations for each type of item
'''
u_reg = r'^u[0-9]*' # this allows for as many response path children as you could possibly want. 
prop_reg = r'&p'    # simple regex for matching the proposal
comm_reg = r'#.*'   # this regex is just to strip comments out of the input file
def_reg = r'~'      # regex for definitions
multiChoice_reg = r'\[([a-z\s"\(\)\\]*,?)+\]'
filename_reg = r'.*\.tangoChat' # This is used as part of a couple of checks that the user file input will work
concept_reg = r'^\~'
inline_concept_reg = r'\~[A-z]+'
parenbracket_reg = r'[\(\[\)\]]'



'''
    Note:
    When writing a tangoChat file, keep in mind that this program tokenizes based off of the ':' character. There MUST
    be a ':' between each segment of a dialogue line, ie type/level:(user responses):program response
    If this is not present in your dialogue file, the program WILL NOT function as intended.
    Additionally, concepts MUST have their possible
'''

class decision_node:
    def __init__(self,type = None, level = -1, parent_level = -1,parent = None, resp = ['--{Begin Conversation, Human}--'], inputs = []):
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
        self.concept_table = {}
        self.amp_found = False
        self.process_file(in_filename)



    def process_file(self,filename):
        try:
            convo_file = open(filename) 
        except expression as identifier:
            print("--{Yeah, it sure doesn't look like this file exists, chief}--")
            print(identifier)
            return

        convo_string = convo_file.readlines()
        tokenized_convo = []
        for line in convo_string:
            temp_line = []
            line = line.strip() # cuts off any newlines from the start or end of the current line
            line = line.split(':',2) # splits a line from type:inputs:response into a list of [type, inputs, response]. Splits only twice, to allow for ':'s in the program response
            for segment in line: 
                segment = segment.strip(" ") # removes any extra spaces surrounding the current line segment
            if re.match(concept_reg,line[0]):
                self.add_concept(line)
            else:
                for segment in line[:-1]: # hacky fix, but allows the program's response to retain its original cases
                    temp_line.append(segment.lower()) # casts the entire row into lowercase to remove any need for case sensitivity
                temp_line.append(line[-1])
                tokenized_convo.append(temp_line)
        self.process_line(tokenized_convo) # Once most of the raw input file has been processed for use, it gets passed here for parsing


    def process_line(self, input_string):
        for line in input_string:
            if line[0] == 'u': # does a small change whenever a 'u' without a number is found, to fit into the code I wrote prior to getting a sample dialogue
                line[0] = 'u0'
            if self.amp_found:
                    raise Exception("--{There is already an & in this text file. Halting execution}--")    
            elif not self.root_generated:
                if not re.match(prop_reg, line[0]):
                    print("--{This isn't a proposal line, checking next}--")
                else:
                    print("--{Proposal line found, beginning tree generation}--")
                    self.amp_found = True
                    self.generate_root(line)
            if re.match(u_reg,line[0]):
                if not self.root_generated:
                    self.root.level= -1
                    self.root_generated = True
                # logic to place dialogue options in the correct place in the tree
                if int(line[0][1]) == self.prev_node.level-1:
                    self.cur_parent = self.cur_parent.parent
                elif int(line[0][1]) == self.prev_node.level+1:
                    self.cur_parent = self.prev_node
                elif int(line[0][1]) < self.prev_node.level+1:
                    while int(line[0][1]) < self.prev_node.level+1:
                        self.prev_node = self.prev_node.parent
                    self.cur_parent = self.prev_node
                self.cur_parent.add_child(self.process_u_node(line,self.cur_parent))
        # if not self.root_generated:


    '''When the above function comes across any 'level' of 'u', it hops into this function to begin adding a new 
        node to the conversation tree'''
    def process_u_node(self,line,parent_node):
        inputs = []
        resp = line[2]
        resp = resp.strip()
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
        if re.match(parenbracket_reg,resp):
            resp = self.process_multi_word(resp)
        new_option = decision_node(type='u',level = level,parent_level=parent_node.level,parent=parent_node,resp=resp,inputs=inputs)
        self.prev_node = new_option
        return new_option
        # parent_node.add_child(new_option)


    # This is perhaps a hacky method, but it splits an input string into individual words, and substrings when denoted with ""
    def process_multi_word(self, line):
        split = []
        in_line = re.sub(parenbracket_reg,'',line)
        last = 0
        first_quote_found = False
        for i in range(len(in_line)):
            temp = ''
            if in_line[i] == '"':
                if not first_quote_found:
                    first_quote_found = True
                    last += 1
                elif first_quote_found:
                    first_quote_found = False
                    temp = in_line[last:i]
                    temp.strip()
                    temp = re.sub(r'\\','',temp)
                    if not re.match(r'\s',temp):
                        split.append(temp)
                    last = i+1
            elif not first_quote_found:
                if re.match(r'\s', in_line[i]):
                    temp = in_line[last:i]
                    temp.strip()
                    temp = re.sub(r'\\','',temp)
                    if not re.match(r'\s',temp):
                        split.append(temp)
                    last = i+1
        return split

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


    # This is used when there are no proposals in the tangochat file
    def generate_user_root(self,line):
        user_root = self.process_u_node(line,decision_node(type = 'dummy', level = 0, parent_level = 0,parent = None, resp = '', inputs = []))
        user_root.parent = None
        self.root = user_root

    def process_concept_input(self,concept,word):
        concept_list = self.concept_table[concept]
        for item in concept_list:
            if word == item:
                return True
        return False

    def pick_concept(self,concept):
        concept_list = self.concept_table[concept]
        return random.choice(concept_list)

    def pick_response(self,responses):
        if isinstance(responses,list):
            return random.choice(responses)
        else:
            return responses

    '''This begins the conversation. It is called "other" because there were other methods that 
        I tried before doing this one, and then I was too lazy to change the name after I was done'''
    def other_converse(self,cur):
        in_resp = str(self.pick_response(cur.resp))
        if re.match(inline_concept_reg, in_resp):
            concept = re.match(inline_concept_reg, in_resp) #redundant, perhaps, but I just wanted to be as specific as possible here
            new_word = self.pick_concept(concept.string[1:])
            in_resp = re.sub(inline_concept_reg,new_word,in_resp)
        print(in_resp)
        if len(cur.children) != 0:
            reply = input().lower()
            for child in cur.children:
                for possible_reply in child.inputs:
                    if re.match(inline_concept_reg,possible_reply):
                        reply_key = re.match(inline_concept_reg,possible_reply)
                        reply_key = reply_key.string[1:]
                        for val in self.concept_table[reply_key]:
                            if reply == val:
                                self.other_converse(child)
                                return
                    elif reply == possible_reply:
                        self.other_converse(child)
                        return
        return

    def add_concept(self, concept):
        #concept = concept.rsplit('')
        concept_name = re.sub(r'\~','',concept[0])
        concept_list = self.process_multi_word(concept[1])
        self.concept_table.update({concept_name:concept_list})

    def traverse(self,par):
        par.__str__()
        for child in par.children:
            self.traverse(child)

    def test_root(self):
        self.root.__str__()

    def print_full_data(self):
        for key in self.concept_table:
            print(key+': '+str(self.concept_table[key]))
        self.traverse(self.root)


        
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
            try:
                convo_tree = decision_tree(toOpen)
                #convo_tree.test_root()
                #convo_tree.traverse(convo_tree.root)
                #convo_tree.print_full_data()
                convo_tree.other_converse(convo_tree.root)
                print("--{Dialogue complete}--")
            except Exception as ident:
                print(ident)
        else:
            print("Your input file does not follow the requirement: *.tangoChat\nPlease try again with the correct filetype")

    

if __name__ == "__main__":
    main()

