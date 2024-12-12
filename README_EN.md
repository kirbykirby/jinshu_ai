<div align="center">


<h1>Jinshu AI</h1>


**English** | [**简体中文**](README.md)

</div>

---

## Prologue
Verily, the Jin Dynasty, though renowned for virtue, suffered heaven's calamities. The central plains were lost, and the five Hu defiled the sacred altars. These events move me to contemplate the fate of ancient realms.

In the year of Jiazi, amid plague and tribulation, I discovered Wang's "History of the Wei, Jin, Northern and Southern Dynasties" and immersed myself in its wisdom. My feeble memory prompted me to record these lessons, aspiring to share Chinese history with the world.

I established an English YouTube channel, drawing from "The Book of Jin." 

Though initially unfamiliar with classical texts, I strove to render their profound meanings in simple English. 

While video editing ultimately forced me to abandon the channel, the translation work persisted in my thoughts.

This spring, though my foray into Python and artificial intelligence was brief, it revealed AI's potential for translation.

Of the vast "Twenty-Four Histories," I have completed only Jinshu's volumes. Is this not a divine providence?

The ancients said, "Many commenced well, but few completed their tasks." Today, with the assistance of AI, I hope to consummate this unfinished work, which would be a great achievement. 

So I wrote these scripts in two days.

Though devoid of innate talent, I wish to emulate Sima Qian and continue the legacy of my forebears, recounting the rise and fall of the Jin Dynasty and elucidating the causes of success and failure. With the aid of AI, I hope to bridge the chasm between ancient and modern times, thereby fulfilling this aspiration.

## Introduction
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
2. Run `clean_md.py` to clean the data.

## Costs
The translation of "Records of Liu Yao" (11,435 characters) cost me ¥4.35, at a rate of ¥0.38 ($0.05) per thousand characters.

Based on this rate, translating the complete Jinshu (1,158,126 characters) would cost approximately ¥440.08 ($61.12).

Due to some LLMs' caching capability, the actual cost would be lower: if the cache is hit, the price is only 10%-50% of the normal rate.

## Important Notes

### 1. Classical Chinese Often Omits Subjects
Fill in the `subject` parameter in the `init_translator_and_translate` function to avoid mistranslating subjects. Example:
```
Original text:
弱冠游于洛阳，坐事当诛，亡匿朝鲜……（《刘曜载记》）

Incorrect translation:
At the age of twenty, [incorrect subject] traveled to Luoyang, where [incorrect subject] faced execution for an offense but fled to Joseon.

Correct translation:
At the age of twenty, Liu Yao traveled to Luoyang, where he faced execution for an offense but fled to Joseon.
```

### 2. AI Occasionally Mistranslates Names/Places by Translating Individual Characters
Example:
```
Original text:
黄石屠各路松多起兵于新平、扶风，聚众数千，附于南阳王保。（《刘曜载记》）

Incorrect translation:
Huangshi slauthered Lusongduo, who raised an army in Xinping and Fufeng, gathering several thousand followers and allied with Prince of Nanyang Bao.
(Incorrectly translates the character "屠" as "slaughter". "Tuge" is a Xiongnu tribe name and should be transliterated as a proper noun.)

Correct translation:
In Huangshi, Lu Songduo of the Tuge raised an army in Xinping and Fufeng, gathering several thousand followers and allied with Prince of Nanyang Bao.
```


### 3. Inconsistent Terminology Translation
```
Original text:
使持节

Translation variations:
Envoy with Imperial Insignia
Envoy with Imperial Credentials
Bearer of Imperial Insignia
...
```

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