import json

# read vocab.json in vocab variable


vocab = json.load(open('vocab.json'))
#print(vocab["object_idx_to_name"][1])
#print(vocab["object_idx_to_name"][35])
#print(vocab["object_idx_to_name"][3])
#print(vocab["object_idx_to_name"][118])

items = []
items.append(vocab["object_name_to_idx"]["man"])
items.append(vocab["object_name_to_idx"]["tree"])
items.append(vocab["object_name_to_idx"]["grass"])
#items.append(vocab["object_name_to_idx"]["field"])
#items.append(vocab["object_name_to_idx"]["background"])
#items.append(vocab["object_name_to_idx"]["ear"])
#items.append(vocab["object_name_to_idx"]["trunk"])
print(items)

print("[1,"+str(vocab["pred_name_to_idx"]["behind"]) + ",0]")
print("[1,"+str(vocab["pred_name_to_idx"]["on top of"]) + ",2]")
#print("[0,"+str(vocab["pred_name_to_idx"]["has"]) + ",5]")
#print("[0,"+str(vocab["pred_name_to_idx"]["has"]) + ",6]")


print("-----------------")

items = []
items.append(vocab["object_name_to_idx"]["box"])
items.append(vocab["object_name_to_idx"]["table"])

print(items)

print("[0,"+str(vocab["pred_name_to_idx"]["on top of"]) + ",1]")
#print("[1,"+str(vocab["pred_name_to_idx"]["near"]) + ",2]")
#print("[0,"+str(vocab["pred_name_to_idx"]["has"]) + ",5]")
#print("[0,"+str(vocab["pred_name_to_idx"]["has"]) + ",6]")