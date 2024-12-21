<div align="center">


<h1>Jinshu AI</h1>


**English** | [**简体中文**](../README.md)

</div>

---

## 🤓 Prologue
I believe the Jin dynasty was blessed with spiritual essence and nurtured excellence. Yet heaven sent down chaos, the four seas were in turmoil, the Five Barbarians held power, the Six Departments lost order, and the Seven Temples fell from grace.

Moved by this, I often contemplate the rise and fall of ancient dynasties.

In the year of Jiazi, when turmoil spread across the land and plague ran rampant, I stayed behind closed doors. 

There I found Wang's "History of Wei, Jin, and the Northern and Southern Dynasties," which I studied day and night, finding much resonance within.

Alas, my memory proves dull, and much was forgotten over time. Thus, I became determined to write, resolved to spread Chinese civilization to all corners of the world.

Despite my limitations, I created a Western YouTube channel, telling our dynasty's stories in English. In my writing, the "Book of Jin" has been my constant companion.

Initially unfamiliar with classical Chinese, I immersed myself in study, translating to English. Through explaining profound principles in simple terms, I began to understand the ancients' true intent.

However, video editing proved to be excessively laborious. Though I temporarily suspended this endeavor, my determination to translate and narrate remained unchanged.

This spring, I learned Python and studied AI algorithms, but with limited energy, this pursuit was shelved.

Recently, during my leisure time, I suddenly realized that AI could assist in my translation work. 

While the Twenty-Four Histories contain a vast collection of forty million words, I have a particular fondness for the hundred and three volumes of the Book of Jin - perhaps this, too, is heaven's will.

The ancients said: "Many begin well, few finish well." Now, with AI's assistance, completing this unfinished work would be splendid! Thus, I spent two days crafting these scripts.

Though lacking in talent, I wish to follow Xuanling's aspiration, chronicle the rise and fall of the Jin, and illuminate the reasons for their success and failure. With AI as my aid, bridging past and present, I hope not to disappoint this heart's resolve.

## 🤔 Introduction
To put it in English, this is a tool that uses AI to translate md files and outputs the translated text in a formatted docx file. 
You can translate any long text using this tool, not just Jinshu. (lol)

## 📑 Usage Guide
1. [Click to Register](https://api.bltcy.ai/register?aff=q3ue) at Bolatu AI to obtain your API key.
   - You can use LLM from OpenAI, Anthropic, Google, etc.
   - The price is over 60% cheaper than the official rate.
2. (Optional) Use an OpenAI API key (you may need to modify the forwarding address).
3. Create a `.env` file and input your API key in `BLT_KEY`.
4. Install the `uv` library ([link](https://github.com/astral-sh/uv)), or [download for Windows users](https://github.com/astral-sh/uv/releases/download/0.5.8/uv-x86_64-pc-windows-msvc.zip).
5. Modify the parameters in `main.py` as needed, and run `uv run main.py` from the command line to start the translation.

## 📚 Data Acquisition
The original text of "The Book of Jin" is available [here](https://ctext.org/wiki.pl?if=gb&res=788577&remap=gb), from the [Chinese Text Project.](https://ctext.org/ens)

This website **strictly prohibits** automatic scraping; you must manually obtain the data.
1. Open a chapter, Ctrl+A, Ctrl+C, Ctrl+V to a markdown file.
2. Run `clean_md.py` to clean the data.

## 💵 Costs
The translation of "Records of Murong Wei" (8,665 characters) cost me ¥2.66, at a rate of ¥0.307 ($0.04) per thousand characters.

Based on this rate, translating the complete Jinshu (1,158,126 characters) would cost approximately ¥355.54 ($48.7).

## ⚠ Important Notes

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

### 2. Occasional Mistranslations of Names/Places by Translating Individual Characters
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
Possible solution: Tell AI to give the original terms as they are, then use a table to replace them with English translations.



## 💬 Project Structure
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

## 🌏 Future Prospects
- [ ] Add custom knowledge base to the context
- [ ] Maintain consistent translation of terminologies (e.g., official titles)
- [ ] Automatic creation of an index of characters
- [ ] Support more translation engines
- [ ] Support the native Anthropic API
- [ ] Add a user interface