# CSCI 455 Assignment 5

## Dialogue Engine

Our implementation utilizes a tree datastructure and regular expressions to build branching dialogue paths of near-infinite (dependent only on system resources) length. It can handle as many U scopes as you can throw at it, so long as they are properly sequenced, i.e. you can't jump from U3 to U7. Concepts can be defined anywhere in the file and still be accessible by any concept call. User inputs can be 

This program was designed to handle any .tangoChat file that follows the conventions laid out in the sample dialogue file from D2L:

- User responses are wrapped in parentheses, i.e. (input)
- Multiple choice user responses are wrapped in ([]) and separated by spaces (commas are not currently supported), i.e. ([yes no "maybe so"])
- Multiple-word responses (only when part of a multiple choice response) for both user and computer are wrapped in double quotes, i.e. "this... is... MULTILINE!!"
  - If only one response (even if multiword) is possible, the quotes can be omitted
- Concept definitions and calls are prefixed by ~
- Concept and proposal definitions only have two sections separated by a :, type and response
  - Proposal:: &p: Hello
  - Concept:: ~OS: [Linux "Everything Else"]
- Each 'section' of a u-line is separated by a :, i.e. U3: (sample input): [multiple options for "machine response"]
  - Leading and trailing whitespace is removed from each of these sections, so go wild with tabs and spaces if that floats your boat


## Running this program

This program must be run with the following command line arguments (testing was done in a unix shell, though this should also work in the windows command line):

> *Note: Replace **inputFile** with the name of the .tangoChat file you would like to use*
```
python3 dialogueMachine.py inputFile.tangoChat
```

This program was primarily developed and tested on python 3.5.2, and has been tested to work on python versions 3.6 and 3.7. It should run on any later versions of python 3 as well.