import os
import pdb
from parse import segment_transcript



def test_correct_output():
 #open the input data
 test_data=os.getcwd()+'/inputs/test_data/input.txt'
 output=segment_transcript(test_data)
 expected_output=[{'unit':"[BEEPING] INTERVIEWER: --they died. I mean--"},{'unit':"SUBJECT 1: I don't--"},{'unit':"INTERVIEWER: But I haven't met any adults. Mostly the children survived. OK, we're rolling. Oh, will you please start by giving your name and--"}]
 assert output == expected_output


if __name__ == '__main__':
 test_correct_output()
