from telethon import TelegramClient, events
import random

# Your Telegram Bot token
BOT_TOKEN = '6826415817:AAG1alKRjdc20hXtYtVT20yowAR2nCnHLWQ'

# Initialize the Telegram client with the bot token
client = TelegramClient('tic_tac_toe_bot', api_id=None, api_hash=None, bot_token=BOT_TOKEN)

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

# Event handler for incoming messages
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await start_game(event)

# Event handler for making a move
@client.on(events.NewMessage(pattern=r'\d \d'))
async def move(event):
    position = tuple(map(int, event.message.text.split()))
    await make_move(event, position)

# Start the client
client.start()
client.run_until_disconnected()
