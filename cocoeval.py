'''
Wrapper for evaluation on CIDEr, ROUGE_L, METEOR and Bleu_N
using coco-caption repo https://github.com/tylin/coco-caption
  
class COCOScorer is taken from https://github.com/yaoli/arctic-capgen-vid
'''

import os, sys
import matplotlib.pyplot as plt

coco_caption_dir = "./coco-caption/"
sys.path.insert(0, coco_caption_dir)

from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer

# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

class COCOScorer(object):
    def __init__(self):
        print 'init COCO-EVAL scorer'
            
    def score(self, GT, RES, IDs):
        self.eval = {}
        self.imgToEval = {}
        gts = {}
        res = {}
        for ID in IDs:
            gts[ID] = GT[ID]
            res[ID] = RES[ID]
        print 'tokenization...'
        tokenizer = PTBTokenizer()
        gts  = tokenizer.tokenize(gts)
        res = tokenizer.tokenize(res)

        # =================================================
        # Set up scorers
        # =================================================
        print 'setting up scorers...'
        scorers = [
            (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
            (Meteor(),"METEOR"),
            (Rouge(), "ROUGE_L"),
            (Cider(), "CIDEr")
        ]

        # =================================================
        # Compute scores
        # =================================================
        eval = {}
        for scorer, method in scorers:
            print 'computing %s score...'%(scorer.method())
            score, scores = scorer.compute_score(gts, res)

            # ...................................................................................
            # boxplot with outliers
            try:
                if scorer.method() == 'Bleu':
                    for i, aux in enumerate(scores):
                        # aux is an array containing 2990 scores, one per test video
                        plt.figure()
                        plt.boxplot(aux, 0, 'gD')
                        plt.title('Scores for method ' + scorer.method() + '(' + str(i) + ')')
                        # plt.show()
                        axes = plt.gca()
                        axes.set_ylim([-0.1, 1.1])
                        plt.savefig('scores_' + scorer.method() + '_' + str(i) + '.png')
            except:
                print '[WARNING] Score boxplots not created due to _tkinter.TclError: no display name and no $DISPLAY environment variable'
            # ...................................................................................

            if type(method) == list:
                for sc, scs, m in zip(score, scores, method):
                    self.setEval(sc, m)
                    self.setImgToEvalImgs(scs, IDs, m)
                    #print "%s: %0.3f"%(m, sc)
            else:
                self.setEval(score, method)
                self.setImgToEvalImgs(scores, IDs, method)
                #print "%s: %0.3f"%(method, score)
                
        for metric, score in self.eval.items():
            print '%s: %.3f'%(metric, score)
        return self.eval
    
    def setEval(self, score, method):
        self.eval[method] = score

    def setImgToEvalImgs(self, scores, imgIds, method):
        for imgId, score in zip(imgIds, scores):
            if not imgId in self.imgToEval:
                self.imgToEval[imgId] = {}
                self.imgToEval[imgId]["image_id"] = imgId
            self.imgToEval[imgId][method] = score