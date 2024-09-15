@pytest.mark.skip(reason='Skipping test by default due to long execution time.')
def test_benchmark():
    import time


        with open('resources/data/snippet.txt') as f:		    with open('./resources/visual/snippet.txt') as f:
            sentences = [x for x in f.read().split('\n') if x]		        sentences = [x for x in f.read().split('\n') if x]


        sentences = [Sentence(x) for x in sentences[:100]]		    sentences = [Sentence(x) for x in sentences[:10]]


        contexts = char_contexts(sentences)		    charlm_embedding_forward = CharLMEmbeddings('news-forward')
    charlm_embedding_backward = CharLMEmbeddings('news-backward')


        with open('resources/data/char_contexts.txt', 'w') as f:		    embeddings = StackedEmbeddings(
            f.write('\n'.join(contexts))		        [charlm_embedding_backward, charlm_embedding_forward]
    )


    def test_benchmark(self):		    tic = time.time()


        import time		    prepare_word_embeddings(embeddings, sentences)


        with open('resources/data/snippet.txt') as f:		    current_elaped = time.time() - tic
            sentences = [x for x in f.read().split('\n') if x]		


        sentences = [Sentence(x) for x in sentences[:10]]		    print('current implementation: {} sec/ sentence'.format(current_elaped / 10))


    embeddings_f = CharLMEmbeddings('news-forward')
    embeddings_b = CharLMEmbeddings('news-backward')


        charlm_embedding_forward = CharLMEmbeddings('news-forward')		    tic = time.time()
        charlm_embedding_backward = CharLMEmbeddings('news-backward')		


        embeddings = StackedEmbeddings(		    prepare_char_embeddings(embeddings_f, sentences)
            [charlm_embedding_backward, charlm_embedding_forward]		    prepare_char_embeddings(embeddings_b, sentences)
        )		


        tic = time.time()		    current_elaped = time.time() - tic


        prepare_word_embeddings(embeddings, sentences)		    print('pytorch implementation: {} sec/ sentence'.format(current_elaped / 10))


        current_elaped = time.time() - tic		


        print('current implementation: {} sec/ sentence'.format(current_elaped / 10))		@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", reason="Skipping this test on Travis CI.")
def test_show_word_embeddings():


        embeddings_f = CharLMEmbeddings('news-forward')		    with open('./resources/visual/snippet.txt') as f:
        embeddings_b = CharLMEmbeddings('news-backward')		        sentences = [x for x in f.read().split('\n') if x]


        tic = time.time()		    sentences = [Sentence(x) for x in sentences]


        prepare_char_embeddings(embeddings_f, sentences)		    charlm_embedding_forward = CharLMEmbeddings('news-forward')
        prepare_char_embeddings(embeddings_b, sentences)		    charlm_embedding_backward = CharLMEmbeddings('news-backward')


        current_elaped = time.time() - tic		    embeddings = StackedEmbeddings([charlm_embedding_backward, charlm_embedding_forward])


        print('pytorch implementation: {} sec/ sentence'.format(current_elaped / 10))		    X = prepare_word_embeddings(embeddings, sentences)
    contexts = word_contexts(sentences)


    trans_ = tSNE()
    reduced = trans_.fit(X)


class Test_show(unittest.TestCase):		    show(reduced, contexts)
    def test_word(self):		


        reduced = numpy.load('resources/data/tsne.npy')		


        with open('resources/data/contexts.txt') as f:		@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", reason="Skipping this test on Travis CI.")
            contexts = f.read().split('\n')		def test_show_char_embeddings():


        show(reduced, contexts)		    with open('./resources/visual/snippet.txt') as f:
        sentences = [x for x in f.read().split('\n') if x]


    def test_char(self):		    sentences = [Sentence(x) for x in sentences]


        reduced = numpy.load('resources/data/char_tsne.npy')		    embeddings = CharLMEmbeddings('news-forward')


        with open('resources/data/char_contexts.txt') as f:		    X_forward = prepare_char_embeddings(embeddings, sentences)
            contexts = f.read().split('\n')		


        show(reduced, contexts)		    embeddings = CharLMEmbeddings('news-backward')


    def test_uni_sentence(self):		    X_backward = prepare_char_embeddings(embeddings, sentences)


        reduced = numpy.load('resources/data/uni_tsne.npy')		    X = numpy.concatenate([X_forward, X_backward], axis=1)


        with open('resources/data/snippet.txt') as f:		    contexts = char_contexts(sentences)
            sentences = [x for x in f.read().split('\n') if x]		


        l = len(sentences[0])		    trans_ = tSNE()
    reduced = trans_.fit(X)


        with open('resources/data/char_contexts.txt') as f:		    show(reduced, contexts)
            contexts = f.read().split('\n')		


        show(reduced[:l], contexts[:l])		


    def test_uni(self):		@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", reason="Skipping this test on Travis CI.")
def test_show_uni_sentence_embeddings():


        reduced = numpy.load('resources/data/uni_tsne.npy')		    with open('./resources/visual/snippet.txt') as f:
        sentences = [x for x in f.read().split('\n') if x]


        with open('resources/data/char_contexts.txt') as f:		    sentences = [Sentence(x) for x in sentences]
            contexts = f.read().split('\n')		


        show(reduced, contexts)		    embeddings = CharLMEmbeddings('news-forward')


    X = prepare_char_embeddings(embeddings, sentences)


class TestHighlighter(unittest.TestCase):		    
    trans_ = tSNE()
    def test(self):		    
        reduced = trans_.fit(X)


        i = numpy.random.choice(2048)
        l = len(sentences[0])

        with open('resources/data/snippet.txt') as f:		    contexts = char_contexts(sentences)
            sentences = [x for x in f.read().split('\n') if x]		

        embeddings = CharLMEmbeddings('news-forward')		    
        show(reduced[:l], contexts[:l])

        features = embeddings.lm.get_representation(sentences[0]).squeeze()		

        Highlighter().highlight_selection(features, sentences[0], n=1000)		def test_highlighter():
        with open('./resources/visual/snippet.txt') as f:
            sentences = [x for x in f.read().split('\n') if x]
            embeddings = CharLMEmbeddings('news-forward')
        qfeatures = embeddings.lm.get_representation(sentences[0]).squeeze()


if __name__ == '__main__':		   
    Highlighter().highlight_selection(features, sentences[0], n=1000, file_='./resources/visual/data/highligh.html')
    unittest.main()		
    shutil.rmtree('./resources/visual/data')




def test_plotting_training_curves_and_weights():
    plotter = Plotter()
    plotter.plot_training_curves('./resources/visual/loss.tsv')
    plotter.plot_weights('./resources/visual/weights.txt')


    # clean up directory
    os.remove('./resources/visual/weights.png')
    os.remove('./resources/visual/training.png')