clear
clc

% Copy names from pdf saved from rons crazy word file
% Paste into bbedit and add ' at beginning and end of line using grep

list = {
'McNeil,Liam Ian Allan'
'Boire,Emily C'
'Gohl,Brandon Joseph'
'Fernandez,Zachary Tyler'
'Taskovski,Stephen M'
'Gurung,Nima'
'Matrulli,Nicholas John'
'Franklin,Kristina M'
'Ventiquattro,Thomas Mike'
'Howell,Gwynneth'
'Melone,Gregory B'
'Koerber,Colton James'
'Zehtab,Ali'
'Myles,Logan'
'Steg,Erich Matthias'
'West,Dylan D'
'Kirsch,John'
'Walzak,Samuel'
'Clark,Jeffrey'
'Yu,Jia Yu'
}

num = 4;
for k=1:num
    shortlist =[];
    for i=k:num:length(list)
        shortlist = [shortlist, sprintf('%s; ',list{i})];
    end
    shortlist
end

