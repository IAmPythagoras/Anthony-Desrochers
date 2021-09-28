import torch
random_action = False
output = torch.tensor([0.9, 0.8])
action_index = [torch.randint(17, torch.Size([]), dtype=torch.int)
                    if random_action
                    else torch.argmax(output)][0]

print(action_index)

print(torch.zeros(0))