% Open and read csv file containing all market data
fid=fopen('MARKETS03.csv','r');
numCols=7;
opts={'Delimiter',','};
headers=textscan(fid,repmat('%s',[1,numCols]),1,opts{:});
data=textscan(fid,['%s' repmat('%f',[1,numCols-1])],opts{:});
fclose(fid);

% Convert dates to timestamps
date=data{1};
date=datenum(date,'mm/dd/yyyy');

% Open and read csv file containing all asset data
mid=fopen('DIAMONDS.csv','r');
MnumCols=28;
Mname=textscan(mid,repmat('%s',[1,MnumCols]),1,opts{:});
Mdata=textscan(mid,['%s' repmat('%f',[1,MnumCols-1])],opts{:},'HeaderLines',1);
fclose(mid);

estData=cell(MnumCols,numCols-1);
teData=cell(MnumCols,numCols-1);
world=data{4};
ftsW=fints(date,world);
worldW=fts2mat(toweekly(ftsW));
wRet=price2ret(worldW);
%wRet=price2ret(world);
garch11=garch(1,1);          % Construct GARCH(1,1) model
est=estimate(garch11,wRet);  % Fitting model
hworld=infer(est,wRet);      % Extract conditional variance from estimation
[r,c]=size(hworld);
q90=prctile(hworld,90);
q95=prctile(hworld,95);
q99=prctile(hworld,99);
gt90=[];
gt95=[];
gt99=[];
% Construct dummy variables
for j=1:r
    if hworld(j,c)>q99
       gt90=[gt90;1];
       gt95=[gt95;1];
       gt99=[gt99;1];
    elseif hworld(j,c)>q95
       gt90=[gt90;1];
       gt95=[gt95;1];
       gt99=[gt99;0];
    elseif hworld(j,c)>q90
       gt90=[gt90;1];
       gt95=[gt95;0];
       gt99=[gt99;0];
    else
       gt90=[gt90;0];
       gt95=[gt95;0];
       gt99=[gt99;0];
    end  
end

for i=2:numCols
    idxName=headers{i};
    p=data{i};
     fts=fints(date,p);            % Convert dates to financial time series
     pW=fts2mat(toweekly(fts));    % Convert daily data to weekly
     idxRet=price2ret(pW(2:end,:));  % Convert prices to log returns   
    %idxRet=price2ret(p(2:end,:));
    ninety=idxRet.*gt90(1:end-1,:);
    ninefive=idxRet.*gt95(1:end-1,:);
    ninenine=idxRet.*gt99(1:end-1,:);
    for m=2:MnumCols
        astName=Mname{m};
        price=Mdata{m};
         Mfts=fints(date,price);
         priceW=fts2mat(toweekly(Mfts));
         aRetW=price2ret(priceW(2:end,:));
        %aRetW=price2ret(price(2:end,:));
        y=aRetW;
        X=[idxRet,ninety,ninefive,ninenine];
        % Model specification
        model=arima('Variance',garch(1,1));
        beta0=[0.01 0.01 0.01 0.01];     % Initial values
        [EstMdl,EstParamCov,logL,info]=estimate(model,y,'X',X,'Beta0',beta0);
        coef=EstMdl.Beta;
        c0=coef(1,1);
        estData{m-1,i-1}=coef;
        ttlef=[];
        for j=2:4
            thiscoef=coef(1,j);
            sum=thiscoef+c0;
            ttlef=[ttlef;sum];
        end
        teData{m-1,i-1}=ttlef;
    end  
end
    