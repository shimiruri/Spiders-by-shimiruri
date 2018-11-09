# Redis address
redis_host = 'localhost'

# Redis port number
redis_port = 6379

# Redis password
redis_passwd = None

redis_key = 'proxies'

# Set max proxy score
max_score = 100

# Set min proxy score
min_score = 0

# Set init proxy score
init_score = 10

# Set request valid code
valid_status = 200

# Set proxy test url,but it should set url what you need crawl
test_url = 'https://www.bilibili.com/'

# Set max test number of testing proxy one times
max_test_count = 50

# Set API information
api_host = '127.0.0.1'
api_port = 5555

# Set test cycle timer
test_cycle = 20

# Set getter cycle timer
getter_cycle = 200

# Set switch of test, getter and api
test_enable = True
getter_enable = True
api_enable = True
