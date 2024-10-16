def push(pilha, item):
    pilha.append(item)
    
def pop(pilha):
    if not pilha:
        raise IndexError("pop em uma pilha vazia")
    else:
        pilha.pop()

def size(pilha):
    return len(pilha)

def is_empty(pilha):
    return len(pilha) == 0