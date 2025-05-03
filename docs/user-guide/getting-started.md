# Getting Started

Welcome to the Italian Anki Decks project! This guide will help you get started with using the Anki decks for learning Italian.

## What is Anki?

[Anki](https://apps.ankiweb.net/) is a free and open-source flashcard program that uses spaced repetition to help you memorize information efficiently. It's particularly effective for language learning.

If you're new to Anki, we recommend checking out the [Anki Manual](https://docs.ankiweb.net/) for a comprehensive guide on how to use Anki.

## Installing Anki

Before you can use the Italian Anki Decks, you need to install Anki:

1. Go to the [Anki website](https://apps.ankiweb.net/)
2. Download the version for your operating system (Windows, macOS, Linux)
3. Install Anki following the instructions for your platform

Anki is also available as a mobile app:
- [AnkiMobile](https://apps.apple.com/us/app/ankimobile-flashcards/id373493387) for iOS (paid)
- [AnkiDroid](https://play.google.com/store/apps/details?id=com.ichi2.anki) for Android (free)

## Getting the Italian Anki Decks

There are two ways to get the Italian Anki Decks:

### Option 1: Download Pre-built Decks

1. Go to the [Releases page](https://github.com/joshrotenberg/italian-anki/releases) on GitHub
2. Download the `.apkg` files for the levels you want (A1, A2, B1, or Basic)
3. Import the `.apkg` files into Anki (see below)

### Option 2: Build the Decks Yourself

If you want to customize the decks or build them yourself:

1. Clone the repository:
   ```bash
   git clone https://github.com/joshrotenberg/italian-anki.git
   cd italian-anki
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate the decks:
   ```bash
   # Build A1 decks:
   python src/generate.py --level a1

   # Build A2 decks:
   python src/generate.py --level a2

   # Build B1 decks:
   python src/generate.py --level b1

   # Build basic decks:
   python src/generate.py --level basic

   # Build all levels:
   python src/generate.py --all
   ```

4. The generated `.apkg` files will be in the `output/` directory

## Importing Decks into Anki

To import the decks into Anki:

1. Open Anki
2. Click on "File" > "Import"
3. Navigate to the location of the `.apkg` file
4. Select the file and click "Open"
5. The deck will be imported into Anki

## Deck Structure

The Italian Anki Decks are organized by CEFR level:

- **A1**: Beginner level
- **A2**: Elementary level
- **B1**: Intermediate level
- **Basic**: Essential vocabulary and phrases

Each level contains multiple decks covering different topics, such as:

- Alphabet
- Numbers
- Colors
- Food
- Grammar
- And more!

## Using the Decks

Once you've imported the decks into Anki, you can start studying:

1. Open Anki
2. Select the deck you want to study
3. Click "Study Now" or "Custom Study"
4. Follow Anki's spaced repetition system to review the cards

### Tips for Effective Learning

- **Study regularly**: Short, daily sessions are more effective than long, infrequent ones
- **Use the audio**: Listen to the pronunciation and repeat it out loud
- **Customize the cards**: Add your own notes, images, or audio to make the cards more memorable
- **Use the tags**: Filter cards by tags to focus on specific topics
- **Adjust the settings**: Customize the number of new cards per day and review intervals to suit your learning pace

## Next Steps

Now that you've set up the Italian Anki Decks, check out the [Using Anki Decks](using-anki-decks.md) guide for more detailed information on how to make the most of these decks for learning Italian.

Happy learning! 🇮🇹