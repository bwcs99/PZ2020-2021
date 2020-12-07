from .client import Client

PORT = 65001
HOST = '127.0.0.1'

test_client = Client()

test_client.sock.connect((HOST, PORT))

test_client.more_money(200, 'edzia') # tu ok !

test_client.less_money(50, 'edzia') # tu  ok !

print(test_client.get_treasury_state('edzia'))

test_client.add_scores(500, 'marcel') # tu ok !

test_client.add_scores(500, 'edzia')

test_client.send_changed([[1, 2], [1, 2], [-1, 1]])

test_client.give_cities('edzia', 'marcel', ['Berlin'])

test_client.get_cities_from_server()

test_client.add_city('edzia', 'Bulgaria')

test_client.end_game_by_host()

#test_client.quit_game('edzia')


