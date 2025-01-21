from __future__ import annotations

import random

from src.Board import Board
from src.InputParser import InputParser
from src.Move import Move
from src.MoveNode import MoveNode

WHITE = True
BLACK = False


class AI:
    depth = 1
    movesAnalyzed = 0

    def __init__(self, board: Board, side: bool, depth: int):
        self.board = board
        self.side = side
        self.depth = depth
        self.parser = InputParser(self.board, self.side)

    def getRandomMove(self) -> Move:
        legalMoves = list(self.board.getAllMovesLegal(self.side))
        randomMove = random.choice(legalMoves)
        return randomMove

    def generateMoveTree(self) -> list[MoveNode]:
        moveTree = []
        for move in self.board.getAllMovesLegal(self.side):
            moveTree.append(MoveNode(move, [], None))

        for node in moveTree:
            self.board.makeMove(node.move)
            self.populateNodeChildren(node)
            self.board.undoLastMove()
        return moveTree

    def populateNodeChildren(self, node: MoveNode) -> None:
        node.pointAdvantage = self.board.getPointAdvantageOfSide(self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            return

        side = self.board.currentSide

        legalMoves = self.board.getAllMovesLegal(side)
        if not legalMoves:
            if self.board.isCheckmate():
                node.move.checkmate = True
                return
            elif self.board.isStalemate():
                node.move.stalemate = True
                node.pointAdvantage = 0
                return
            raise Exception()

        for move in legalMoves:
            self.movesAnalyzed += 1
            node.children.append(MoveNode(move, [], node))
            self.board.makeMove(move)
            self.populateNodeChildren(node.children[-1])
            self.board.undoLastMove()

    def bestMovesWithMoveTree(self, moveTree: list[MoveNode]) -> list[Move]:
        bestMoveNodes: list[MoveNode] = []
        alpha = float('-inf')
        beta = float('inf')
        
        for moveNode in moveTree:
            moveNode.pointAdvantage = self.minimax(moveNode, self.depth, alpha, beta, True)
            
            if not bestMoveNodes:
                bestMoveNodes.append(moveNode)
            elif moveNode > bestMoveNodes[0]:
                bestMoveNodes = []
                bestMoveNodes.append(moveNode)
            elif moveNode == bestMoveNodes[0]:
                bestMoveNodes.append(moveNode)

        return [node.move for node in bestMoveNodes]

    def minimax(self, node: MoveNode, depth: int, alpha: float, beta: float, maximizingPlayer: bool) -> int:
        if depth == 0 or not node.children:
            return self.evaluatePosition(node)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in node.children:
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for child in node.children:
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def evaluatePosition(self, node: MoveNode) -> int:
        score = node.pointAdvantage
        
        # Bonus for controlling center
        if node.move.newPos[0] in [3,4] and node.move.newPos[1] in [3,4]:
            score += 0.5
            
        # Bonus for development in opening
        old_pos = self.board.pieceAtPosition(node.move.oldPos)
        if node.depth < 10 and (old_pos is None or old_pos.stringRep != 'P'):
            score += 0.3
            
        # Penalty for moving same piece twice in opening
        moves_to_check = min(node.depth, len(self.board.history))
        if node.depth < 10 and node.move.piece in [m[0].piece for m in self.board.history[-moves_to_check:] if m[0].piece]:
            score -= 0.2
            
        return int(score * 100)

    def getBestMove(self) -> Move:
        moveTree = self.generateMoveTree()
        bestMoves = self.bestMovesWithMoveTree(moveTree)
        
        # Filter moves that lead to checkmate first
        checkmateMoves = [move for move in bestMoves if move.checkmate]
        if checkmateMoves:
            bestMove = random.choice(checkmateMoves)
            bestMove.notation = self.parser.notationForMove(bestMove)
            return bestMove
            
        # Consider positional factors for other moves
        scoredMoves = []
        for move in bestMoves:
            score = 0
            
            # Prefer moves that control the center
            if move.newPos[0] in [3,4] and move.newPos[1] in [3,4]:
                score += 1
                
            # Prefer moves that develop pieces in opening
            if self.board.movesMade < 10 and move.piece.stringRep in ['N','B']:
                score += 1
                
            # Discourage moving pieces multiple times in opening
            if self.board.movesMade < 10 and any(move.piece == m[0].piece for m in self.board.history):
                score -= 1
                
            scoredMoves.append((move, score))
            
        # Get moves with highest score
        maxScore = max(score for _, score in scoredMoves)
        bestMoves = [move for move, score in scoredMoves if score == maxScore]
        
        bestMove = random.choice(bestMoves)
        bestMove.notation = self.parser.notationForMove(bestMove)
        return bestMove

    def makeBestMove(self) -> None:
        self.board.makeMove(self.getBestMove())


if __name__ == '__main__':
    mainBoard = Board()
    ai = AI(mainBoard, True, 3)
    print(mainBoard)
    ai.makeBestMove()
    print(mainBoard)
    print(ai.movesAnalyzed)
    print(mainBoard.movesMade)
