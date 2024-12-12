# Jinshu AI Translator
**English** | [**简体中文**](README.md)


## Prologue
Verily, the Jin Dynasty was renowned for its magnanimity and virtue. Nevertheless, heaven visited calamities upon it, causing the central plains to be lost, and the five Hu to vie for supremacy, thereby defiling the sacred altars. Moved by these events, I oftentimes reflect upon the rise and fall of ancient realms.

In the year of Jiazi, the world was beset by tribulations, and the plague spread far and wide. Confining myself within the precincts of my study, I acquired Wang’s "A History of the Wei, Jin, Northern and Southern Dynasties." I perused it day and night, and oftentimes found it to be replete with wisdom. Regrettably, my memory is feeble, and after protracted reading, much was forgotten. Thus, I resolved to commit these lessons to parchment, and vowed to disseminate the chronicles of Chinese history across the globe.

Unwilling to demean myself, I established an English YouTube channel to elucidate the narratives of our dynasties. Whenever I wrote, I frequently relied upon "The Book of Jin." Initially, I was unversed in the classical tongue but diligently studied and translated it into English. My aim was to expound lofty concepts in simple terms, thus elucidating the intentions of the ancients.

Subsequently, the laborious task of video editing compelled me to discontinue the channel. However, the translation work continued to preoccupy my thoughts. This spring, I learned Python and delved into the principles of artificial intelligence, but my energies were limited, and I put the project on hold.

Recently, with some respite, I suddenly conceived of the potential of AI to aid my translation endeavors. In the "Twenty-Four Histories," which encompass millions of words, I have but read "The Book of Jin"'s one hundred and thirty volumes from beginning to end. Is this not a divine providence?

The ancients said, "Many commenced well, but few completed their tasks." Today, with the assistance of AI, I hope to consummate this unfinished work, which would be a great achievement. So I completed this script in two days.

Though devoid of innate talent, I wish to emulate Sima Qian and continue the legacy of my forebears, recounting the rise and fall of the Jin Dynasty and elucidating the causes of success and failure. With the aid of AI, I hope to bridge the chasm between ancient and modern times, thereby fulfilling this aspiration.

## Introduction
Introduction
To put it in English, this is a tool that uses AI to translate md files and outputs the translated text in a formatted docx file. 
In fact, you can translate any type of document using this tool lol

## Usage Guide
1. [Click to Register](https://api.bltcy.ai/register?aff=q3ue) at Bolatu AI to obtain your API key.
   - You can use LLM from OpenAI, Anthropic, Google, etc.
   - The price is over 60% cheaper than the official rate.
2. (Optional) Use an OpenAI API key (you may need to modify the forwarding address).
3. Create a `.env` file and input your API key in `BLT_KEY`.
4. Install the `uv` library ([link](https://github.com/astral-sh/uv)), or [download for Windows users](https://github.com/astral-sh/uv/releases/download/0.5.8/uv-x86_64-pc-windows-msvc.zip).
5. Modify the parameters in `main.py` as needed, and run `uv run main.py` from the command line to start the translation.

## Data Acquisition
The original text of "The Book of Jin" is available [here](https://ctext.org/wiki.pl?if=gb&res=788577&remap=gb), from the "Project for the Electronic Textualization of Chinese Philosophy."

This website **strictly prohibits** automatic scraping; you must manually obtain the data.
1. Open a chapter, Ctrl+A, Ctrl+C, Ctrl+V to a markdown file.
2. Remove any extraneous text at the beginning and end, ensuring each paragraph starts with a number.

## Costs
For example, translating "The Biography of Liu Yao" took 11,435 characters and cost ¥4.35 (¥0.38 or $0.05 per thousand characters).

## Project Structure
```
|- README.md # Project overview
|- main.py # Main script
|- translator # Translation module
| |- init.py # Initialization file
| |- chatbot.py # Chatbot module
| |- config.py # Configuration file
| |- formatter.py # Formatting module
| |- prompts.py # Prompt module
| |- translator.py # Translation script
| |- utils.py # Utility module
|
|- pyproject.toml # Project dependencies file
|- uv.lock # uv dependencies file
```

## Future Prospects
- [ ] Add custom knowledge base to the context
- [ ] Maintain consistent translation of terminologies (e.g., official titles)
- [ ] Automatic creation of an index of characters
- [ ] Support more translation engines
- [ ] Support the native Anthropic API
- [ ] Add a user interface
- 