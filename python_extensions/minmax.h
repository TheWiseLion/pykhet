#ifndef MINMAX_H_INCLUDED
#define MINMAX_H_INCLUDED
#include <Python.h>
#include "search.h"
#include <stdlib.h>
#include <stdio.h>
#define MAX(a,b) ((a) > (b) ? a : b)
#define MIN(a,b) ((a) < (b) ? a : b)
//#include <queue>
//#include <ctime>
//#include <map>
//#include <algorithm>

/***
* Functions For Preforming Alpha-Beta Search with the worlds **sh@ttiest** huerisitic
* It may also be useful to keep a hash at each node so identical boards arent explored more than once.
*/

int get_minimum_leaf(struct BoardContainer * bc, char color){
    struct Node * n = &bc->nodes[0];
//    Node c = *n;
    float seekValue;
    int indexChild;
    int index;
    float h;
    int i;

    //Edge Case - Root has no children
    if(n->numChildern == 0){
        return n->nodeIndex;
    }

    //Step one find the min value from root


    //Trace the value down to leaf
    while(n->fin != 1 && n->expanded){ //In theory num children could still be zero...
        index = -1;

        seekValue = (n->color==_red)?-100000.0f : 100000.0f;
        for (i=0; i < n->numChildern; i++){
            indexChild = n->childIndicies[i];
            h = bc->nodes[indexChild].nodeHueristic;
            if(n->color==_silver && seekValue > h){
                //Choose Min node
                seekValue = h;
                index = indexChild;

            }else if(n->color==_red && seekValue < h){
                //Chose Max node
                seekValue = h;
                index = indexChild;

            }
        }

        n = &bc->nodes[index];
    }

    return n->nodeIndex;
}

void updateHueristic(int nodeIndex,struct BoardContainer * bc){
    int reachedRoot = 0;
    int updateIndex = nodeIndex;
    struct Node * update;
    float value;
    int diff;
    int c;
    unsigned int indexChild;
    //Add bias if a move leads to
    //more potential mistakes by opponent add a slight weight to it
    //Makes for better openings...
    int positiveCount = 0;
    int negativeCount = 0;
    float hueristic;


    while(!reachedRoot){
        //Hueristic to promotes move where your opponent has "less" good moves
        positiveCount = negativeCount = 0;
        update = &bc->nodes[updateIndex];
        value = (update->color==_red)?-100000.0f:100000.0f;
        for(c=0; c < update->numChildern; c++){
            indexChild = update->childIndicies[c];
            //Difference Between Raw Score (parent - child)
            diff = bc->nodes[indexChild].boardHueristic - update->boardHueristic;
            hueristic = bc->nodes[indexChild].nodeHueristic;

            if(update->color == _silver){
                value = MIN(value, hueristic);
            }else{
                value = MAX(value, hueristic);
            }

             //add a 5x multiplier if it causes player to lose
            if(diff > 0){
                positiveCount += 1 + (diff==1000)*5;
            }else if(diff < 0){
                negativeCount += 1 + (diff==-1000)*5;
            }
        }

        update->nodeHueristic = value + (positiveCount-negativeCount)*0.008f; //Score + bias
//        printf("Bias: %f v %f\n", (positiveCount-negativeCount)*0.008f,update->nodeHueristic);

//        if(update->nodeHueristic < -1){
//            printf("Favor: %i, %i\n",update->nodeIndex,update->depth);
//        }
        reachedRoot = (update->parentIndex == -1);
        updateIndex = update -> parentIndex;
    }
}

// Input Initial State
// Output move ratings
struct MoveRating{
    int moveValue;
    float moveRating;
};

struct MoveResults{
    int numMoves;
    struct MoveRating * moves;
};

struct Queue{
    int size;
    int limit;
    int * lst;
};

struct Queue * newQueue(int size){
    struct Queue * q = (struct Queue*)malloc(sizeof(struct Queue));
    q->size = 0;
    q->limit = size;
    q->lst = (int*) malloc(size * sizeof(int));
    return q;
}

int pop(struct Queue * q){
    int v = q->lst[q->size-1];
    q->size -= 1;
    return v;
}

void push(struct Queue * q, int i){
    int newLimit;
    int * old;
    int * n;
    if(q->size + 1 >= q->limit){
        newLimit = q->limit *2;
        old = q->lst;
        n = (int*) malloc(q->size * sizeof(int));
        memcpy(n,old, q->size*sizeof(int));
        q->limit = newLimit;
        free(old);
    }

    q->lst[q->size] = i;
    q->size+=1;
}


struct MoveResults getMoveRatings(char color, char * intialBoard, int minDepth, int iterations){
    struct BoardContainer bc;
    //Allocate slightly more since when we expand the last node...
    int iterationWithSafety = iterations + 118;
    int index;
    int c=0;
    int i;
    int lastNode = -1;
    int minLeaf;
    struct Node * n;
    unsigned int indexChild;
    struct MoveResults mr;
    struct Node * root;
    struct Queue * q;
    int lastPrint = 0;
    bc.boards = (char*) malloc(sizeof(char) * 80 * iterationWithSafety);
    bc.nodes = (struct Node*) malloc(sizeof(struct Node) * iterationWithSafety);

    //Create the root of the tree...
    bc.nodes[0].numChildern = 0;
    bc.nodes[0].color = color;
    bc.nodes[0].parentIndex = -1;
    bc.nodes[0].depth = 1;
    bc.nodes[0].nodeIndex = 0;
    bc.nodes[0].boardHueristic = 0;
    bc.numBoards = 1;
    bc.limit = iterationWithSafety;
    memcpy(bc.boards,intialBoard, 80);

    q = newQueue(30000);
    push(q,0);

    //Step 1 First we explore to the minimum depth...
    while(q->size > 0
         && bc.nodes[q->lst[q->size-1]].depth <= minDepth
         && iterations > bc.numBoards){

        index = pop(q);
        n = &bc.nodes[index];
        expand_node(n, &bc);

        // Loop Through Children.


        for(c=0; c < n->numChildern; c++){
            indexChild = n->childIndicies[c];
            bc.nodes[indexChild].nodeHueristic = bc.nodes[indexChild].boardHueristic;
//            printf("Board %i v. h %f\n",bc.nodes[indexChild].boardHueristic,bc.nodes[indexChild].nodeHueristic);
            //If not end node?
            if(bc.nodes[indexChild].depth <= minDepth){
                push(q,indexChild);
            }

        }

        // Update Tree Heuristic (lg N) MinMax
        updateHueristic(n->nodeIndex, &bc);

    }

    //printf("%i iterations used to reach depth %i with %i queued\n",bc.numBoards,minDepth,q->size);




    //Step 2 we do iterative deepening search
    while(iterations > bc.numBoards){ //TODO: need a condition to escape when no more moves...
        if(lastPrint + 10000 < bc.numBoards){
            lastPrint = bc.numBoards;
            //printf("%f complete...\n",(float)bc.numBoards/iterations);
        }

        //LG(N)
        minLeaf = get_minimum_leaf(&bc, color);
        if(lastNode == minLeaf || bc.nodes[minLeaf].fin){
            //printf("Can't expand?\n %i... %i... expanded:%i C:%i fin:%i, H:%i HC: %f\n",
                  // minLeaf, bc.numBoards,bc.nodes[minLeaf].expanded,
                  // bc.nodes[minLeaf].numChildern, bc.nodes[minLeaf].fin,
                  // bc.nodes[minLeaf].boardHueristic, bc.nodes[minLeaf].nodeHueristic);
            get_minimum_leaf(&bc, color);
            break;
        }else{
            // O(~C)
            expand_node(&bc.nodes[minLeaf], &bc);
            // O(Lg N)
            updateHueristic(minLeaf, &bc);
        }
        lastNode = minLeaf;

    }

    minLeaf = get_minimum_leaf(&bc, color);

    //printf("%i iterations used to reach depth %i\n",bc.numBoards, bc.nodes[minLeaf].depth);

    //printf("%i min leaf with h-score %f\n",minLeaf, bc.nodes[minLeaf].nodeHueristic);


    root = &bc.nodes[0];
    mr.numMoves = root->numChildern;

    mr.moves = (struct MoveRating*)malloc(sizeof(struct MoveRating) * root->numChildern);
    for(i=0; i  < root->numChildern; i++){
        n = &bc.nodes[root->childIndicies[i]];
        mr.moves[i].moveRating = n->nodeHueristic;
        mr.moves[i].moveValue = n->moveValue;
    }

    free(q->lst);
    free(q);
    free(bc.boards);
    free(bc.nodes);
    return mr;
}


#endif // MINMAX_H_INCLUDED
