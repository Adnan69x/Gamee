from telethon.sync import TelegramClient, events
import random

# Your Telegram API credentials
API_ID = '24851795'
API_HASH = 'fe711257cd657bcc2b9244c2b5efc151'

# Your Telegram Bot token
BOT_TOKEN = '6826415817:AAG1alKRjdc20hXtYtVT20yowAR2nCnHLWQ'

# Initialize the Telegram client for user session
client = TelegramClient('user_session', API_ID, API_HASH)

# Initialize the Telegram client for bot session
client_bot = TelegramClient('bot_session', BOT_TOKEN)

# Dictionary to store ongoing games
games = {}

# Function to start a new game
async def start_game(event):
    chat_id = event.chat_id
    player1 = event.sender_id
    player2 = None
    game_board = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
    turn = 1
    message = await event.respond("Tic Tac Toe XOX game started! Waiting for another player...")
    games[chat_id] = {'player1': player1, 'player2': player2, 'board': game_board, 'turn': turn, 'message': message}

# Function to make a move
async def make_move(event, position):
    chat_id = event.chat_id
    player = event.sender_id
    if chat_id in games:
        game = games[chat_id]
        if game['player2'] is None:
            await event.respond("Waiting for another player to join...")
        elif player != game['player1'] and player != game['player2']:
            await event.respond("You are not part of this game.")
        elif player == game['player1'] and game['turn'] == 2:
            await event.respond("It's not your turn.")
        elif player == game['player2'] and game['turn'] == 1:
            await event.respond("It's not your turn.")
        else:
            row, col = position
            if game['board'][row][col] != ' ':
                await event.respond("That position is already taken.")
            else:
                symbol = 'X' if player == game['player1'] else 'O'
                game['board'][row][col] = symbol
                game['turn'] = 2 if game['turn'] == 1 else 1
                await update_board(chat_id)
                winner = check_winner(game['board'])
                if winner is not None:
                    await event.respond(f"Player {winner} wins!")
                    del games[chat_id]
                elif ' ' not in [cell for row in game['board'] for cell in row]:
                    await event.respond("It's a draw!")
                    del games[chat_id]

# Function to update the game board
async def update_board(chat_id):
    game = games[chat_id]
    board = game['board']
    message = game['message']
    board_str = "\n".join([" | ".join(row) for row in board])
    await message.edit(f"Tic Tac Toe XOX Game\n{board_str}")

# Function to check for a winner
def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

# Event handler for incoming messages in user session
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await start_game(event)

# Event handler for making a move in user session
@client.on(events.NewMessage(pattern=r'\d \d'))
async def move(event):
    position = tuple(map(int, event.message.text.split()))
    await make_move(event, position)

# Start the user session client
client.start()

# Event handler for incoming messages in bot session
@client_bot.on(events.NewMessage(pattern='/start'))
async def start_bot(event):
    await start_game(event)

# Event handler for making a move in bot session
@client_bot.on(events.NewMessage(pattern=r'\d \d'))
async def move_bot(event):
    position = tuple(map(int, event.message.text.split()))
    await make_move(event, position)

# Start the bot session client
client_bot.start()
client_bot.run_until_disconnected()
