% Open and read csv file containing all market data
fid=fopen('MARKETS03.csv','r');
numCols=6;
opts={'Delimiter',','};
headers=textscan(fid,repmat('%s',[1,numCols]),1,opts{:});
data=textscan(fid,['%s' repmat('%f',[1,numCols-1])],opts{:});
fclose(fid);

% Convert dates to timestamps
date=data{1};
date=datenum(date,'mm/dd/yyyy');

% Open and read csv file containing all asset data
mid=fopen('METALS03.csv','r');
MnumCols=6;
Mname=textscan(mid,repmat('%s',[1,MnumCols]),1,opts{:});
Mdata=textscan(mid,['%s' repmat('%f',[1,MnumCols-1])],opts{:},'HeaderLines',1);
fclose(mid);

estData=cell(MnumCols,numCols-1);

allMkRet=[];
allaRet=[];

% Loop through each market
for i=2:numCols
    idxName=headers{i};
    p=data{i};
%     fts=fints(date,p);          % Convert dates to financial time series
%     weekly=toweekly(fts);
%     weeklyDates=weekly.dates;
%     pW=fts2mat(weekly);          % Convert daily data to weekly
    retW=price2ret(p);            % Convert prices to log returns
    [r,c]=size(retW);
    allMkRet=[allMkRet,retW];
    allMkFts=fints(date(2:end,:),allMkRet);
%     allMkFts=fints(weeklyDates(2:end,:),allMkRet);
    q10=prctile(retW,10);
    q5=prctile(retW,5);
    q1=prctile(retW,1);
    lt10=[];
    lt5=[];
    lt1=[];
    % Construct dummy variables
    for j=1:r
        if retW(j,c)<q1
            lt10=[lt10;1];
            lt5=[lt5;1];
            lt1=[lt1;1];
        elseif retW(j,c)<q5
            lt10=[lt10;1];
            lt5=[lt5;1];
            lt1=[lt1;0];
        elseif retW(j,c)<q10
            lt10=[lt10;1];
            lt5=[lt5;0];
            lt1=[lt1;0];
        else
            lt10=[lt10;0];
            lt5=[lt5;0];
            lt1=[lt1;0];
        end  
    end
    
    ten=retW.*lt10;
    five=retW.*lt5;
    one=retW.*lt1;
    
    % Loop through each asset
    for m=2:MnumCols
        astName=Mname{m};
        price=Mdata{m};
%          Mfts=fints(date,price);
%          priceW=fts2mat(toweekly(Mfts));
        aRet=price2ret(price);
        allaRet=[allaRet,aRet];
        allaFts=fints(date(2:end,:),allaRet);
%         allaFts=fints(weeklyDates(2:end,:),allaRet);
        y=aRet;
        X=[retW,ten,five,one];
        % Model specification
        model=arima('Variance',garch(1,1));
        beta0=[0.01 0.01 0.01 0.01];          % Initial values
        [EstMdl,EstParamCov,logL,info]=estimate(model,y,'X',X,'Beta0',beta0);
        estData{m-1,i-1}=EstMdl.Beta; 

    end  
end
