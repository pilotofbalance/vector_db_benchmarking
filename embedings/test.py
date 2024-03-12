from sentence_transformers import SentenceTransformer
import json

sentences = []
f = open('train_set.json')
data = json.load(f)

for item in data:
    sentence = "input:" + item["input"] + " |||| otput:" + item["output"]
    sentences.append(sentence)

print("SENTENCES IS READY")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
dictionary = []
for sentence, embedding in zip(sentences, embeddings):
    record = {
        "sentence": sentence,
        "embedding": embedding.tolist()
    }
    dictionary.append(record)
    
with open("sample.json", "w") as outfile:
    json.dump(dictionary, outfile)


# sentences = [
#     "abdominal aortic aneurysm (aaa)",
#     "thoracic aortic aneurysm (taa)",
#     "lymphadenopathy",
#     "pulmonary embolism",
#     "dense breasts",
#     "lymphoma in children and young adults",
#     "alzheimer's disease",
#     "diffuse interstitial lung disease",
#     "cardiomegaly",
#     "pleural effusion",
#     "diverticulitis",
#     "osteonecrosis",
#     "splenomegaly",
#     "endometrial cancer",
#     "bone metastasis",
#     "coronary artery occlusion",
#     "endometriosis",
#     "ovarian cancer",
#     "appendicitis",
#     "enlarged prostate (bph)",
#     "pancreatic cancer",
#     "arthritis",
#     "brain tumor",
#     "liver metastasis",
#     "infiltrative opacification of lungs",
#     "esophageal cancer",
#     "enlarged parathyroid gland ",
#     "brain metastasis",
#     "fatty liver disease",
#     "peripheral artery disease (pad)",
#     "breast cancer",
#     "fecal incontinence",
#     "pneumonia",
#     "breast lumps",
#     "gallstones",
#     "polycystic ovary",
#     "carotid artery stenosis",
#     "liver fibrosis",
#     "prostate cancer",
#     "cervical cancer",
#     "head injury",
#     "lung metastasis",
#     "cholecystitis",
#     "polyps of sinus",
#     "renal artery stenosis",
#     "cirrhosis of the liver",
#     "fungal sinusitis",
#     "renal cysts",
#     "rectal tumor",
#     "liver cysts",
#     "brain artery occlusion",
#     "lung bulla",
#     "bronchoectasis",
#     "lung emphysema",
#     "proctitis",
#     "deep vein thrombosis",
#     "small intestine obstruction",
#     "bowel perforation",
#     "lung nodules",
#     "vascular malformations",
#     "pelvic mass"
# ]
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# embeddings = model.encode(sentences)

# dictionary = []
# for sentence, embedding in zip(sentences, embeddings):
#     record = {
#         "sentence": sentence,
#         "embedding": embedding.tolist()
#     }
#     dictionary.append(record)
    
# with open("query.json", "w") as outfile:
#     json.dump(dictionary, outfile)