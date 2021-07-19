%% Import Script for ODF Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.
clear
%% Specify Crystal and Specimen Symmetries

% crystal symmetry
%m-3m for cubic
CS = crystalSymmetry('6/m', [0 0 1], 'color', 'light blue');

% specimen symmetry
SS = specimenSymmetry('triclinic');

% plotting convention
setMTEXpref('xAxisDirection','east');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = pwd;

% which files to be imported
fname = [pname '\EulerAngles.txt'];

%% Import the Data

% specify kernel
psi = deLaValleePoussinKernel('halfwidth',10*degree);
cop=orientation.byMiller([1,1,2],[1,1,1],CS,SS);
s=orientation.byMiller([1,2,3],[6,3,4],CS,SS);
brass=orientation.byMiller([0,1,1],[1,1,2],CS,SS);
goss=orientation.byMiller([0,1,1],[1,0,0],CS,SS);
bss=orientation.byMiller([1,6,8],[2,1,1],CS,SS);
bsg=orientation.byMiller([0,1,1],[5,1,1],CS,SS);
tcu=orientation.byMiller([5,5,2],[1,1,5],CS,SS);
cube=orientation.byMiller([1,0,0],[0,1,0],CS,SS);
basal=orientation.byEuler(00*degree,00*degree,00*degree,CS,SS);
% create an EBSD variable containing the data
% odf = ODF.load(fname,CS,SS,'density','kernel',psi,'resolution',2*degree,...
%   'interface','generic',...
%   'ColumnNames', { 'phi1' 'Phi' 'phi2'}, 'Bunge', 'Radians', 'Active Rotation');
odf=1*unimodalODF(basal,psi)%+ 0.0*unimodalODF(goss,psi)+ 0.0*unimodalODF(s,psi)+0.0*unimodalODF(cop,psi)+0.1*uniformODF(CS,SS)+0.0*unimodalODF(brass,psi)+0.0*unimodalODF(bss,psi)+0.17*unimodalODF(bsg,psi)+0.06*unimodalODF(tcu,psi);
%loop
%sample values such that they sum to 1
%create odf according to command below:
% export the data to DRX-{i}.txt


% odf=0.9*unimodalODF(brass,psi)+0.1*unimodalODF(goss,psi);
%% Correct Data
figure
plotPDF(odf,Miller({1,0,0},{1,1,0},{0,0,1},CS),'contourf','upper');
rot = rotation('Euler',00*degree,90*degree,90*degree);
colormap
%odf = rotate(odf,rot);
%%
fname='DRX-1.txt';
S3G = equispacedSO3Grid(CS,'resolution',5*degree);
export(odf,fname,S3G,'Bunge','generic');
fprintf('done');