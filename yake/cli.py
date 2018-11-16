from yake import KeywordExtractor
import glob, os, argparse

def readDoc(docpath):
	with open(docpath, encoding='utf8') as infile:
		return infile.read()

def getlan(datasetpath):
	with open(os.path.join(datasetpath,'..','lan.txt'), encoding='utf8') as infile:
		return infile.read()[:2]

def getdocid(docpath):
	return os.path.basename(docpath).rsplit('.',1)[0]

def getdatasetid(datasetpath):
	return os.path.dirname(datasetpath).split(os.path.sep)[-2]

def getname(n, w, dedupLim, dedupFunc, features, allfeats):
	allfeats = set(allfeats)
	features = set(features)
	names = ['NonC']

	for feat in allfeats:
		if feat not in features:
			names.append('non'+feat)

	if len(names) > 0:
		print(n, w, dedupFunc, dedupLim, '_'.join(names) )
		return 'n%d_w%d_%s-%.2f_f-%s' % (n, w, dedupFunc, dedupLim, '_'.join(names) )
		
	return 'n%d_w%d_%s-%.2f' % (n, w, dedupFunc, dedupLim)

allfeats =["WRel", "WFreq", "WSpread", "WCase", "WPos", "KPF"]

parser = argparse.ArgumentParser()
required_args = parser.add_argument_group('required arguments')
required_args.add_argument('-i','--input', type=str, nargs='+', help='Dataset docs directory.', required=True)

parser.add_argument('-df','--dedup-func', type=str, nargs='?', help='Deduplication function.', default='seqm', choices=['leve', 'jaro', 'seqm'])
parser.add_argument('-dl','--dedup-lim', type=float, nargs='?', help='Deduplication limiar.', default=.9)

parser.add_argument('-ws','--windows-size', type=int, nargs='?', help='Windows size.', default=1)
parser.add_argument('-n','--ngram-size', type=int, nargs='?', help='Max size of the ngram.', default=3)
parser.add_argument('-t','--top', type=int, nargs='?', help='Max size of rank.', default=10)
parser.add_argument('-f','--features', type=str, nargs='+', help='Features to use.', default=allfeats, choices=allfeats)

parser.add_argument('-o','--output', type=str, nargs='?', help='Output directory.', default='../output/Yake/')

args = parser.parse_args()
print(args)
#lan="en", n=3, dedupLim=0.8, dedupFunc='levenshtein', windowsSize=2, top=20, features=None
nameApp = getname(n=args.ngram_size, w=args.windows_size, dedupLim=args.dedup_lim, dedupFunc=args.dedup_func, features=args.features, allfeats=allfeats)

for datasetpath in args.input:
	datasetname = getdatasetid(datasetpath)
	lan=getlan(datasetpath)
	yake = KeywordExtractor(lan=lan, windowsSize=args.windows_size, top=args.top, n=args.ngram_size, dedupLim=args.dedup_lim, dedupFunc=args.dedup_func, features=args.features)
	outputpath = os.path.join(args.output, nameApp)
	if not os.path.exists(outputpath):
		os.mkdir(outputpath) 
	outputpath = os.path.join(args.output, nameApp, datasetname)
	if not os.path.exists(outputpath):
		os.mkdir(outputpath) 
	docs2read = sorted(glob.glob(os.path.join(datasetpath,'*')))
	print(datasetname, len(docs2read), nameApp, lan)
	for (i, docpath) in enumerate(docs2read):
		docid = getdocid(docpath)
		outputdoc = os.path.join(outputpath, docid)
		doccontent = readDoc(docpath)
		results = yake.extract_keywords_on(doccontent)
		with open(outputdoc, 'w') as outfile:
			for (h,kw) in results:
				outfile.write('%s %f\n' % (kw, h))
		print("\r%.2f%%" % (100.*i/len(docs2read)), end='... ')
	print("DONE!")
