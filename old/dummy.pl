%   --- PROTOTYPE DUMMY APP for Compass-IO - tool for evaluating ethical implications and assisting ethical decision-making ---
%   This Prolog code serves as a dummy application for Compass-IO.
%   It defines events, harms, harm types, and various models to evaluate the severity of harms.
%   The engine can determine whether an event should be flagged based on the selected model.   

% CALL WITH 
% ?- consult('dummy.pl'). 
% false: don't flag. true: flag. 
% ?- should_flag(surveillance).
% ?- should_flag(automated_firing).
% ?- should_flag(creating_predetermined_breaking_point).

% --- EVENTS ---
event(surveillance).
event(automated_firing).
event(creating_predetermined_breaking_point).

% --- HARMS ---
harms(surveillance, user).
harms(automated_firing, employee).
harms(creating_predetermined_breaking_point, environment).

% --- HARM TYPES ---
harm_type(surveillance, privacy_loss).
harm_type(automated_firing, economic_ruin).
harm_type(environment, environmental_ruin).
harm_type(environmental_ruin, economic_ruin).  % recursive chain

% --- CHAINED HARM RESOLUTION ---
derived_harm_type(A, B) :- harm_type(A, B).
derived_harm_type(A, C) :- harm_type(A, B), derived_harm_type(B, C).

% --- MODEL DEFINITIONS ---
economic_security_model(privacy_loss, 4).
economic_security_model(economic_ruin, 9).

animal_empathy_model(privacy_loss, 2).
animal_empathy_model(economic_ruin, 3).
animal_empathy_model(cat_harm, 10000). 

climate_model(privacy_loss, 1). 
climate_model(economic_ruin, 1). 
climate_model(environmental_ruin, 9). 

anti_capitalist_model(privacy_loss, 8). 
anti_capitalist_model(economic_ruin, 8). 
anti_capitalist_model(environmental_ruin, 9). 

% --- ACTIVE MODEL SELECTOR ---
use_model(economic_security_model).

% --- SCORE FETCHING ---
model_score(Type, Score) :-
    use_model(Model),
    call(Model, Type, Score).

% --- REASONING RULES ---
should_flag(Event) :-
    harm_type(Event, Type),
    model_score(Type, Score),
    Score >= 7.

should_flag(Event) :-
    harms(Event, Entity),
    derived_harm_type(Entity, Type),
    model_score(Type, Score),
    Score >= 7.

% --- END OF DUMMY APP ---