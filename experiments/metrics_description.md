# Evaluation metrics descriptio


**Source:** https://arxiv.org/pdf/1612.07600.pdf

## Metrics

| Metric                            | Proposed to evaluate         | Underlying idea                   |
| --------------------------------- | ---------------------------- | --------------------------------- |
| BLEU (Papineni et al., 2002)      | Machine translation          | n-gram precision                  |
| ROUGE (Lin, 2004)                 | Document summarization       | n-gram recall                     |
| METEOR (Banerjee and Lavie, 2005) | Machine translation          | n-gram with synonym matching      |
| CIDEr (Vedantam et al., 2015)     | Image description generation | tf-idf weighted n-gram similarity |

All these metrics except SPICE and WMD define the similarity over words or n-grams of reference and candidate descriptions by considering different formulas. On the other hand, SPICE (Anderson et al., 2016) considers a scene-graph representation of an image by encoding objects, their attributes and relations between them, and WMD leverages word embeddings to match groundtruth descriptions with generated captions.

### 2.1 BLEU

BLEU (Papineni et al., 2002) is one of the first metrics that have been in use for measuring similarity between two sentences. It has been initially proposed for machine translation, and defined as the geometric mean of n-gram precision scores multiplied by a brevity penalty for short sentences. There exists a smoothed version of BLEU described in (Lin and Och, 2004).

### 2.2 ROUGE

ROUGE (Lin, 2004) is initially proposed for evaluation of summarization systems, and this evaluation is done via comparing overlapping n-grams, word sequences and word pairs. In this study, we use ROUGE-L version, which basically measures the longest common subsequences between a pair of sentences. Since ROUGE metric relies highly on recall, it favors long sentences, as also noted by (Vedantam et al., 2015).

### 2.3 METEOR

METEOR (Banerjee and Lavie, 2005) is another machine translation metric. It is defined as the harmonic mean of precision and recall of unigram matches between sentences. Additionally, it makes use of synonyms and paraphrase matching. METEOR addresses several deficiencies of BLEU such as recall evaluation and the lack of explicit word matching. n-gram based measures work reasonably well when there is a significant overlap between reference and candidate sentences; however they fail to spot semantic similarity when the common words are scarce. METEOR handles this issue to some extent using WordNet-based synonym matching, however just looking at synonyms may be too restrictive to capture overall semantic similarity.

### 2.4 CIDEr

CIDEr (Vedantam et al., 2015) is a recent metric proposed for evaluating the quality of image descriptions. It measures the consensus between candidate image description ci and the reference sentences, which is a set Si = {si1, . . . , sim} provided by human annotators. For calculating this metric, an initial stemming is applied and each sentence is represented with a set of 1-4 grams. Then, the co-occurrences of n-grams in the reference sentences and candidate sentence are calculated. In CIDEr, similar to tf-idf, the n-grams that are common in all image descriptions are downweighted. Finally, the cosine similarity between n-grams (referred as CIDErn) of the candidate and the references is computed.

CIDEr is designed as a specialized metric for image captioning evaluation, however, it works in a purely linguistic manner, and only extends existing metrics with tf-idf weighting over n-grams. This sometimes causes unimportant details of a sentence to be weighted more, resulting in a relatively ineffective caption evaluation.
