#ifndef SEARCH_H_INCLUDED
#define SEARCH_H_INCLUDED

/****
* Board State Values
* Board is 10 x 8
* Value at a position: occupied | orientation | piece type | color
*/
//typedef enum { 0, 1 } char;
char _silver = 1;
char _red = 0;
char _color_mask = 1;

char _pharaoh = 2; // Piece Index - 0
char _anubis = 4; // Piece Index - 1
char _scarab = 6; // Piece Index - 2
char _pyramid = 8; // Piece Index - 3
char _sphinx = 10; // Piece Index - 4
char _type_mask = 14;

// Orientations
char _up = 0;
char _right = 16;
char _down = 32;
char _left = 48;
char _orientation_mask = 48;

// Empty
char _vacant = 0;
char _occupied = -128;
char _vacant_mask = -128;

// Stuff For A Hueristic On Who's Winning
static int PIECE_TO_VALUE[5] = {
    1000, // Pharaoh
    3, // Anubis
    0, //Scarab -> Not a destroyable piece...
    2, // Pyramid
    0 //Sphinx -> Not a destroyable piece...
};

int piece_to_hueristic_value(char piece){
    return PIECE_TO_VALUE[(piece/2)-1];
}


/****
* Helper functions to go to/from compressed value to representation
*/

int _is_vacant(char square){
    return  0 == (_vacant_mask & square);
}

int _is_occupied(char square){
    return (_vacant_mask & square) != 0;
}

char _is_piece(char square, char piece_type){
    return (_type_mask & square) == piece_type;
}

char _piece(char square){
    return square & _type_mask;
}

char _color(char square){
    return square & _color_mask;
}

char _orientation(char square){
    return square & _orientation_mask;
}

char opposite_color(char color){
    if(color == _red){
        return _silver;
    }else{
        return _red;
    }
}


/***
*
* Functions Revolving Around Laser & Piece Orientations
*
*/

char _flip_sphinx_silver(char orientation){
    // If it's left then it's right, if it's up then it's down...
    if (_down == orientation)
        return _right;
    else
        return _down;
}

char _flip_sphinx_red(char orientation){
    // If it's left then it's right, if it's up then it's down...
    if (_left == orientation)
        return _up;
    else
        return _left;
}

char _add_90(char orientation){
    // sooo clutch
    return (orientation + 16) & _orientation_mask;
}

char _sub_90(char orientation){
    // TODO: should be possible with bitwise operators..
    char value = orientation - 16;
    if (value > 0)
        return value;
    else
        return (char)0;
}

char _opposite_direction(char direction){
    if (direction == _up){
        return _down;
    }else if (direction == _down){
        return _up;
    }else if(direction == _left){
        return _right;
    }else{
        return _left;
    }
}

/***
* Determines Bounce Direction When Hitting A Piece
* Returns -1 when it's hit a non-reflective face
*/
char bounce_direction(char piece,char orientation,char light_direction){
    if (piece == _pyramid){
        if (light_direction == _up)
            if (orientation == _down)
                return _left;
            else if (orientation == _right)
                return _right;
            else
                return -1;
        else if (light_direction == _down)
            if (orientation == _left)
                return _left;
            else if (orientation == _up)
                return _right;
            else
                return -1;
        else if (light_direction == _left)
            if (orientation == _right)
                return _down;
            else if (orientation == _up)
                return _up;
            else
                return -1;
        else //Right
            if (orientation == _down)
                return _down;
            else if (orientation == _left)
                return _up;
            else
                return -1;

    }else if (piece == _scarab){
        if (orientation == _down || orientation == _up)
            if (light_direction == _up)
                return _left;
            else if ( light_direction == _down)
                return _right;
            else if ( light_direction == _left)
                return _up;
            else //right
                return _down;

        else
            if (light_direction == _up)
                return _right;
            else if ( light_direction == _down)
                return _left;
            else if ( light_direction == _left)
                return _down;
            else
                return _up;
    }
    return -1;
}

/***
* Some squares only allow certain color...
*/
char color_matches_square(char color,int x1,int y2){
    if (color == _red && (x1 == 0 || (y2 == 0 && x1 == 9) || (y2 == 7 && x1 == 9)))
        return 0;
    else if (color == _silver && (x1 == 9 || (y2 == 0 && x1 == 2) || (y2 == 7 && x1 == 2)))
        return 0;
    else
        return 1;
}

/***
*
* Game Logic Helper Functions
*
*/


//mmm my life for Aiur
struct Position{
    int x,y;
};

/**
* Get next laser position given a location and moving direction
*/
struct Position next_position(int x, int y,char direction){
    struct Position pos;
    pos.x = x; pos.y = y;

    if (direction == _up){
        pos.y -= 1;
    }else if (direction == _down){
        pos.y += 1;
    }else if (direction == _left){
        pos.x -= 1;
    }else{
        pos.x += 1;
    }

    return pos;
}

/***
* Functions & Structures Around Keeping Search State
*/

// Encode an x and y position in 16 bits (could fit in 8)
short encodePosition(int x, int y){
//    printf("Encode (%i,%i) as %i\n",x,y,(x << 8 | y));
    return x << 8 | y;
}

// Gets the x position from a compressed 'move'
short decodeX(int value){
    return value >> 8;
}

// Gets the x position from a compressed 'move'
short decodeY(int value){
    return value & 0xFF;
}



struct Node{
    char fin; //Cannot Be Expand Further. (Game Over)
    char expanded;
    unsigned char depth;
    char color;
    int boardHueristic;
    float nodeHueristic; // Calculated Based on children/tree.
    int parentIndex;
    int nodeIndex;
    unsigned char numChildern;
    int moveValue;
    int childIndicies[117];
    //Max number of valid moves:
    //12 * 8 (12 pieces that at most can move to 8 adj squares)
    //+ 1 rotatable sphinx
    //+ 10 * 2 (~10 pieces that can rotate 2 directions)
    // Total: 117
};

/**
* Sets move value for node...
*/
void setMoveValue(char rotate, int position, int value, struct Node * m){
//    printf("pos: %i - v: %i\n", position,value);
    int v =  (((int)rotate) << 31) | position << 16 | value;
    m->moveValue = v;
}


/**
* Container for all boards
* Board is layed out as a 80 byte array [x == i%10][y == i/10]
*/
struct BoardContainer{
    char * boards;
    struct Node * nodes;
    int limit;
    int numBoards;

};

//All offsets for spaces around a square
static const int offsetIndex[8] ={
    1,  // x+1
    -1, // x-1
    10, // y+1
    -10,// y-1
    -9, // y-1, x+1
    11, // y+1, x+1
    9,  // x-1, y+1
    -11 // x-1, y-1
};

void printMove(int moveValue){
    char rotate = moveValue >> 31;
    int p = (moveValue >> 16) & 0x7FFF;
    int postitionX = decodeX(p);
    int postitionY = decodeY(p);
    int value = moveValue & 0xFFFF;
    if (rotate){
        printf("(%i,%i) rotates %i degrees\n",postitionX,postitionY, value);
    }else{
        int vx = decodeX(value);
        int vy = decodeY(value);
        printf("(%i,%i) moves to %i,%i\n",postitionX,postitionY,vx,vy);
    }



}

/***
* Creates A New Board By Copying The Index Of An Existing Board
*
*/
int copy_board(struct Node * n, struct BoardContainer * container){
    struct Node * newNode;
    int boardToCopy = n->nodeIndex;
    int newBoard = container->numBoards;
    container->numBoards += 1;
//    printf("Creating new board [%i] from [%i]\n",newBoard,boardToCopy);

    //Start of New Board (destination),Start Address of existing (source), Board Size
    memcpy(&container->boards[newBoard*80],&container->boards[boardToCopy*80],80);

    newNode = &container->nodes[newBoard];
    newNode->parentIndex = boardToCopy;
    newNode->color = opposite_color(n->color);
    newNode->numChildern = 0;
    newNode->nodeIndex = newBoard;
    newNode->depth = n->depth + 1;
    newNode->fin = 0;
    newNode->expanded = 0;

    n->childIndicies[n->numChildern] = newBoard;
    n->numChildern += 1;

    return newBoard;
}

//Full Index From x, y & which board/node index
int totalIndex(int x, int y, int nodeIndex){
    return nodeIndex*80 + x%10 + 10*y;
}

//whether an x,y value is in the bounds of the board
char in_bounds(int x, int y){
    return x < 0 || x > 9 || y < 0 || y > 7;
}

/***
*
* Applies the effect of the laser and updates the hueristic value for the node by the factor of the destroyed piece
* Returns the change in value of the hueristic
*/
int apply_laser(int x, int y, char * board, char direction, int boardIndex){
    /***
    Directly Modifies Board by applying the laser
    :param x:- Local Quordinate
    :param y:- Local Quordinate
    :param board:
    :param direction:
    :return:
    ***/
    struct Position p;
    int h = 0;
    char value;
    int tIndex;
    char piece_type;
    char orientation;
    char bValue;
    p.x = x; p.y = y;

    while (direction != -1){
        p = next_position(p.x, p.y, direction);
        if (in_bounds(p.x, p.y))
            return 0;
        tIndex = totalIndex(p.x,p.y,boardIndex);
        value = board[tIndex];
        if (_is_occupied(value)){
            piece_type = _piece(value);
            orientation = _orientation(value);
            direction = bounce_direction(piece_type, orientation, direction);
            // Piece is if direction is none, hit if any of the piece/orientations are found:
            if ((direction == -1) &&
                (piece_type == _pharaoh ||
                 piece_type == _pyramid ||
                 (piece_type == _anubis && orientation != _opposite_direction(direction))
                 )){
                bValue = board[tIndex];
                h = piece_to_hueristic_value(_piece(bValue)) * (_color(bValue)==_red? -1 : 1);
                board[tIndex] = _vacant; //Destroyed Piece, Apply Delta On Hueristic....
                break;
            }
        }
    }

    return h;
}

/**
* Expand Node. Loops over every piece,
* if piece matches node color will permutate on all moves, then move to the next square
* Returns number of child nodes
*/
int expand_node(struct Node * n, struct BoardContainer * board){
    char invariant = n->color + _occupied;
    char isRed = n->color == _red;
    int boardBoundLower = n->nodeIndex * 80 - 1;
    int boardBoundUpper = n->nodeIndex * 80 + 80;
    int baseIndex;
    char value;
    char piece;
    char orientation;
    char pInvariant;
    int targetPos;
    int xOff;
    int yOff;
    int newBoard;
    int newIndex;
    char tmp;
    int y=0;
    int x=0;
    int i;
    int newOrientation;
    char newValue;
    char rotateLeft;
    char rotateRight;
    struct Node * child;
    char sphinxOrientation;
    int hdelta;

    // Permutate All The Positions And Orientations
    for (y=0; y<8; y++){
        for (x=0; x<10; x++){

            baseIndex = totalIndex(x,y,n->nodeIndex);
            value = board->boards[baseIndex];
//            printf("Expand Node Loop [%i] %i,%i -> %i-%i\n",baseIndex,x,y,_is_occupied(value),_color(value));

            if(_is_occupied(value) && _color(value) == n->color){
                piece = _piece(value);
                orientation = _orientation(value);
                pInvariant = invariant + piece;

                if(piece == _pyramid || piece == _pharaoh || piece == _anubis){
                    //Move Piece
                    for(i = 0; i < 8; i++){
                        targetPos = offsetIndex[i] + baseIndex;
                        xOff = (targetPos-n->nodeIndex*80) % 10;
                        yOff = (targetPos-n->nodeIndex*80) / 10;
                        if(boardBoundLower < targetPos && targetPos < boardBoundUpper && _is_vacant(board->boards[targetPos]) && color_matches_square(n->color,xOff,yOff)){
                            newBoard = copy_board(n, board);
                            newIndex = totalIndex(x,y,newBoard);
                            board->boards[newIndex] = _vacant;
                            board->boards[newIndex + offsetIndex[i]] = value;


                            setMoveValue(0,encodePosition(x,y),encodePosition(xOff, yOff), &board->nodes[newBoard]);
                        }
                    }
                }else if(piece == _scarab){
                    //Swap Pieces
                    for(i = 0; i < 8; i++){
                        targetPos = offsetIndex[i] + baseIndex;
                        xOff = (targetPos-n->nodeIndex*80) % 10;
                        yOff = (targetPos-n->nodeIndex*80) / 10;

                        if(boardBoundLower < targetPos && targetPos < boardBoundUpper && color_matches_square(n->color,xOff,yOff)
                           &&
                           //Can only swap squares with pyramids & anubis (or move to vacant spot)
                           (_piece(board->boards[targetPos]) == _anubis ||
                            _piece(board->boards[targetPos]) == _pyramid ||
                            board->boards[targetPos]==_vacant)){

                            newBoard = copy_board(n, board);
                            newIndex = totalIndex(x,y,newBoard);
                            tmp = board->boards[newIndex + offsetIndex[i]];
                            board->boards[newIndex] = tmp;
                            board->boards[newIndex + offsetIndex[i]] = value;

                            setMoveValue(0,encodePosition(x,y),encodePosition(xOff, yOff), &board->nodes[newBoard]);
                        }
                    }

                    //Rotate Pieces (all rotations are equiv)
                    newOrientation = _add_90(orientation);
                    newValue = pInvariant + newOrientation;
                    newBoard = copy_board(n, board);
                    newIndex = totalIndex(x,y,newBoard);
                    board->boards[newIndex] = newValue;

                    setMoveValue(1,encodePosition(x,y),newOrientation, &board->nodes[newBoard]);


                }else{ //Sphinx
                    newOrientation = (isRed? _flip_sphinx_red(orientation) : _flip_sphinx_silver(orientation));
//                    printf("Rotate Sphinx %i  - %i to %i\n", isRed, orientation, newOrientation);
                    newValue = pInvariant + newOrientation;
                    newBoard = copy_board(n, board);
                    newIndex = totalIndex(x,y,newBoard);
                    board->boards[newIndex] = newValue;

                    setMoveValue(1,encodePosition(x,y),newOrientation, &board->nodes[newBoard]);
                }

                // If pieces that rotate
                if(piece == _pyramid || piece == _anubis){
                    rotateLeft = pInvariant + _add_90(orientation);
                    newBoard = copy_board(n, board);
                    newIndex = totalIndex(x,y,newBoard);
                    board->boards[newIndex] = rotateLeft;
                    setMoveValue(1,encodePosition(x,y),_add_90(orientation), &board->nodes[newBoard]);


                    rotateRight = pInvariant + _sub_90(orientation);
                    newBoard = copy_board(n, board);
                    newIndex = totalIndex(x,y,newBoard);
                    board->boards[newIndex] = rotateRight;
                    setMoveValue(1,encodePosition(x,y),_sub_90(orientation), &board->nodes[newBoard]);

                }

            }
        }
    }

    // Apply The Laser For Each Board...
    //For each child...
//    printf("Expand Node: %i  children\n",n->numChildern);
    for(i=0; i<n->numChildern; i++){
        child = &board->nodes[n->childIndicies[i]];
        x = 0;
        y = 0;
        if(isRed){
            x=9;
            y=7;
        }

        sphinxOrientation = _orientation(board->boards[totalIndex(x,y,n->childIndicies[i])]);
        hdelta = apply_laser(x,y,board->boards, sphinxOrientation,n->childIndicies[i]);
        if (abs(hdelta) == PIECE_TO_VALUE[0]){
            //Reached end game (some one lost their pharaoh)
//            printf("FIN: %i - %i\n", child->nodeIndex,hdelta);
            child ->fin = 1;
            child ->expanded = 1;
        }

        child -> boardHueristic = n->boardHueristic + hdelta;
        child -> nodeHueristic = n -> boardHueristic; // Initialize node heuristic as board heuristic.
    }

    //TODO: Update Parent
    n->expanded = 1;
    return n->numChildern;
}



//TODO: There is a missing edge case when the scarab is on a colored tile and it swaps pieces with an opposite color.
//Though nothing in the official rule book mentions what should actually happen in this scenario....
//Either way I've chosen to ignore this case for now....

#endif // SEARCH_H_INCLUDED
