# Blackjack-Simulator

Final Project - MATH 3808 W21

# Instructions for Use 
- Coming soon

## Project Info

### Members
- Eren Sulutas - 101101873
- Nabeel Warsalee - 101103167
- Cailyn Edwards - 100956026
- Henry Wang

### Professor
- Zhicheng Gao

### Due Date
April 23rd 2021 at 14:00

### Dependencies 
- [PyDealer](https://pydealer.readthedocs.io/)

# Description

This project is focused on computing the House Edge for the casino game Blackjack while using the basic strategy.

Our method for computing the House Edge will be to create a Montecarlo experiment in which we run multiple trials of a Blackjack game having the player utilize the basic strategy.
From these multiple trials, we extract the win/lose probabilities for both Dealer and Player and from that are able to compute the House Edge.

# Blackjack Rules Assumed
- Single deck
- Dealer stands on any 17 (including soft 17)
- Split up to four hands
- Double down on any two initial cards, except for split Aces
- Surrender not permitted 

# Basic Strategy Used
![image](https://user-images.githubusercontent.com/28713150/115052421-ee53d600-9eab-11eb-8bb7-58221b2db225.png)

[Source](https://wizardofodds.com/games/blackjack/strategy/1-deck/)
