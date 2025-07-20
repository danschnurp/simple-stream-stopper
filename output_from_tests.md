


## Tests

### Algorithm Tests

#### TEST 1: Basic example from the task
- **Input tokens**: `['Ah', 'oj, ', 'sv', 'ete', '!']`
- **Stop words**: `['svet']`
- **Original text**: `'Ahoj, svete!'`
- **Result**: `['Ah', 'oj, ']`
- **Filtered text**: `'Ahoj, '`
- **Expected**: `'Ahoj, '` (stops before 'svet')

#### TEST 2: Realistic text stream - news article
- **Input tokens**: `['Pr', 'e', 'ziden', 't Če', 'ské ', 'rep', 'ub', 'liky dnes', ' p', 'odepsal no']...`
- **Stop words**: `['digitalizaci', 'občanů']`
- **Original text**: `'Prezident České republiky dnes podepsal nový zákon o digitalizaci. Změny se dotknou všech občanů a budou platit od příštího roku. Vláda očekává úspory v řádu miliard korun.'`
- **Result**: `['Pr', 'e', 'ziden', 't Če', 'ské ', 'rep', 'ub', 'liky dnes', ' p', 'odepsal no']...`
- **Filtered text**: `'Prezident České republiky dnes podepsal nový zákon o '`
- **Expected**: text up to the first stop word

#### TEST 3: Subword tokenization (BPE-like)
- **Input tokens**: `['Č', 'esk', 'á', ' repub', 'lika', ' má', ' bohat', 'ou', ' hist', 'orii', '.', ' Pra', 'ha', ' je', ' krás', 'né', ' měs', 'to', ' s', ' mnoha', ' památ', 'kami', '.']`
- **Stop words**: `['historie', 'Praha']`
- **Original text**: `'Česká republika má bohatou historii. Praha je krásné město s mnoha památkami.'`
- **Result**: `['Č', 'esk', 'á', ' repub', 'lika', ' má', ' bohat', 'ou', ' hist', 'orii', '.', ' ']`
- **Filtered text**: `'Česká republika má bohatou historii. '`
- **Expected**: text up to 'historie' or 'Praha'

#### TEST 4: Streaming chat with emojis
- **Input tokens**: `['Ahoj', ' všichni', ' 😊', ' Jak', ' se', ' máte', '?', ' Dnes', ' je', ' krásný', ' den', ' ☀️', ' Těším', ' se', ' na', ' víkend', '!', ' Zastavte', ' prosím', ' spam', '.']`
- **Stop words**: `['spam', 'reklama']`
- **Original text**: `'Ahoj všichni 😊 Jak se máte? Dnes je krásný den ☀️ Těším se na víkend! Zastavte prosím spam.'`
- **Result**: `['Ahoj', ' všichni', ' 😊', ' Jak', ' se', ' máte', '?', ' Dnes', ' je', ' krásný', ' den', ' ☀️', ' Těším', ' se', ' na', ' víkend', '!', ' Zastavte', ' prosím', ' ']`
- **Filtered text**: `'Ahoj všichni 😊 Jak se máte? Dnes je krásný den ☀️ Těším se na víkend! Zastavte prosím '`
- **Expected**: text up to 'spam'

#### TEST 5: Code stream with comments
- **Input tokens**: `['def', ' process', '_data', '(', 'data', '):', '\n ', '# ']`
- **Stop words**: `['TODO', 'optimalizovat']`
- **Original text**: `'def process_data(data): # '`
- **Result**: `'def process_data(data): # '`
- **Filtered text**: `'def process_data(data): # '`
- **Expected**: code up to 'TODO' or 'optimalizovat'

#### TEST 6: High-frequency stream with small tokens
- **Input tokens**: `['T', 'o', 't', 'o', ' ', 'j', 'e', ' ']`
- **Stop words**: `['je']`
- **Original text**: `'Toto je '`
- **Result**: `'Toto je '`
- **Filtered text**: `'Toto je '`
- **Expected**: stops at the first stop word

#### TEST 7: Multilingual stream
- **Input tokens**: `['Hello', ' world', '! ', 'Ahoj', ' světe', '! ', 'Здравствуй', ' ']`
- **Stop words**: `['world', 'světe', 'Здравствуй']`
- **Original text**: `'Hello world! Ahoj světe! Здравствуй '`
- **Result**: `'Hello world! Ahoj světe! Здравствуй '`
- **Filtered text**: `'Hello world! Ahoj světe! Здравствуй '`
- **Expected**: text up to the first stop word

#### TEST 8: Performance test - large volume stream
- **Input tokens**: 25000 tokens
- **Stop words**: `['STOP_WORD']`
- **Original text**: 25000 tokens
- **Result**: 25000 tokens
- **Filtered text**: 25000 tokens
- **Expected**: 25000 tokens (stops at STOP_WORD)

### Benchmark Tests

#### Benchmark 1: Effect of number of stop words on performance
- **1 stop word**: 0.0962s, 10000 tokens
- **5 stop words**: 0.0915s, 10000 tokens
- **10 stop words**: 0.0970s, 10000 tokens
- **20 stop words**: 0.0919s, 10000 tokens
- **50 stop words**: 0.0916s, 10000 tokens

#### Benchmark 2: Effect of stop word length
- **Length 5**: 0.0923s, 10000 tokens
- **Length 10**: 0.0907s, 10000 tokens
- **Length 20**: 0.1178s, 10000 tokens
- **Length 30**: 0.1665s, 10000 tokens
- **Length 50**: 0.2222s, 10000 tokens

## real streaming api test

### Basic Stop Word Filtering
- **Input text**: `'Prvním krokem odpovím, že hlavním městem Česka je Praha. Nyní napišu text o této magnifikentné metropoli: Praha, hlavní město Česka, je místo bohaté kulturní a historické hodnoty. Ležící u řeky Vltavy, se svými desítkami věží, zámků a katedrál, přitahuje miliony turistů každoročně. Od barokních оргаňálek v katedrálách po moderní architekturu, Praha nabízí smyslové dojmy pro všechny smysly. Harrachovská ulička s jejími barokními domy, Velká jeruzalémská synagoga s jejími elegantními věžicemi, Letenská zahrada se svým slavnostním vinexem, či Strahovská knihovna s jejími unikátními rukopisy. Kamenny mosty s pohledem na řeku Vltavu, torturovny v Alejích a romanticní Kafkaovy kavárny, všechny spolu tvoří unikátní Prahu. Toto se už nezobrazuje. HOTOVO!'`
- **Stop words**: `['HOTOVO!', 'stopni', 'Praha']`
- **Filtered text**: `'Prvním krokem odpovím, že hlavním městem Česka je '`