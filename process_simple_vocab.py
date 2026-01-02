
import json

with open('simple_extracted_data.json', 'r') as f:
    data = json.load(f)

images = [x['path'] for x in data if x['type'] == 'image']
texts = []
processed_texts = set()

# Normalize text function to handle slight variations if needed
def normalize(text):
    return text.strip()

for x in data:
    if x['type'] == 'text':
        t = normalize(x['value'])
        # Only add if it's not a direct repeat of the immediately preceding text
        # (The json shows "Fom", "Fom" repeatedly, likely duplicates)
        if not texts or texts[-1] != t:
            texts.append(t)

print(f"Total Images: {len(images)}")
print(f"Total Unique Text Blocks: {len(texts)}")

print("\n--- Proposed Alignment (First 20) ---")
for i in range(min(len(images), len(texts), 20)):
    print(f"Image: {images[i]} <-> Text: {texts[i]}")

if len(images) != len(texts):
    print("\nWARNING: Mismatch in counts!")
    print("Extra Images:" if len(images) > len(texts) else "Extra Texts:")
    diff = abs(len(images) - len(texts))
    # print last few to see where it breaks?
