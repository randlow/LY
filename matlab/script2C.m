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
ref=data{2};
% fts=fints(date,ref);        % Convert dates to financial time series
% temp=toweekly(fts);         % Convert to weekly dates
% weekly=temp.dates;
d08=[];
d11=[];
for d=1:length(date)-1
    thisdate=datetime(date(d,:),'ConvertFrom','datenum');
    if isbetween(thisdate,datetime(2008,09,12),datetime(2008,10,22))==1
        d08=[d08;1];
        d11=[d11;0];
    elseif isbetween(thisdate,datetime(2011,07,23),datetime(2011,09,01))==1
        d11=[d11;1];
        d08=[d08;0];
    else
        d08=[d08;0];
        d11=[d11;0];
    end
end

% Open and read csv file containing all asset data
mid=fopen('DIAMONDS.csv','r');
MnumCols=28;
Mname=textscan(mid,repmat('%s',[1,MnumCols]),1,opts{:});
Mdata=textscan(mid,['%s' repmat('%f',[1,MnumCols-1])],opts{:},'HeaderLines',1);
fclose(mid);

estData=cell(MnumCols,numCols-1);
teData=cell(MnumCols,numCols-1);
for i =2:numCols
    idxName=headers{i};
    p=data{i};
%     ftsp=fints(date,p);           % Convert dates to financial time series
%     pW=fts2mat(toweekly(ftsp));   % Convert daily data to weekly
%     idxRet=price2ret(pW);           % Convert prices to log returns 
    idxRet=price2ret(p);
    oheight=idxRet.*d08;
    oneone=idxRet.*d11;
    for m=2:MnumCols 
        astName=Mname{m};
        price=Mdata{m};
%         Mfts=fints(date,price);
%         priceW=fts2mat(toweekly(Mfts));
%         aRet=price2ret(priceW);
        aRet=price2ret(price);
        y=aRet;
        X=[idxRet,oheight,oneone];
        % Model specification
        model=arima('Variance',garch(1,1));
        beta0=[0.01 0.01 0.01];           % Initial values
        [EstMdl,EstParamCov,logL,info]=estimate(model,y,'X',X,'Beta0',beta0);
        coef=EstMdl.Beta;
        c0=coef(1,1);
        estData{m-1,i-1}=coef;
        ttlef=[];
        for j=2:3
            thiscoef=coef(1,j);
            sum=thiscoef+c0;
            ttlef=[ttlef;sum];
        end
        teData{m-1,i-1}=ttlef;    % Construct table consists of all total effect data
    end
end

