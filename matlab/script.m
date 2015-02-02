fid=fopen('markets.csv','r');
numCols=12;
opts={'Delimiter',','};
headers=textscan(fid,repmat('%s',[1,numCols]),1,opts{:});
data=textscan(fid,['%s' repmat('%f',[1,numCols-1])],opts{:});
fclose(fid);

date=data{1}(1:end-1,:);
date=datenum(date,'mm/dd/yyyy');

mid=fopen('METALS.csv','r');
MnumCols=5;
Mname=textscan(mid,repmat('%s',[1,MnumCols]),1,opts{:});
Mdata=textscan(mid,['%s' repmat('%f',[1,MnumCols-1])],opts{:},'HeaderLines',1);
fclose(mid);
assetRet=[];

rid=fopen('result.txt','at');

% for m=2:MnumCols
%     price=Mdata{m};
%     aRet=price2ret(price);
%     Mfts=fints(date,aRet);
%     aRetW=fts2mat(toweekly(Mfts,'EOW',2));
%     assetRet=[assetRet,aRetW];
% end

allRet=[];
for i=2:numCols
    idxName=headers{i};
    p=data{i};
    ret=price2ret(p);
    allRet=[allRet,ret];
    fts=fints(date,ret);
    retW=fts2mat(toweekly(fts,'EOW',2));
    [r,c]=size(retW);
    q10=prctile(retW,10);
    q5=prctile(retW,5);
    q1=prctile(retW,1);
    lt10=[];
    lt5=[];
    lt1=[];
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
    %for k=1:MnumCols-1
       % y=assetRet(:,k);
    for m=2:MnumCols
        astName=Mname{m};
        price=Mdata{m};
        aRet=price2ret(price);
        Mfts=fints(date,aRet);
        aRetW=fts2mat(toweekly(Mfts,'EOW',2));
        y=aRetW;
        X=[retW,lt10,lt5,lt1];
        modelfun=@(b,x)b(1)+b(2).*x(:,1)+b(3).*x(:,1).*x(:,2)+b(4).*x(:,1).*x(:,3)+b(5).*x(:,1).*x(:,4);
        beta0=[0.01 0.01 0.01 0.01 0.01];
        mdl=fitnlm(X,y,modelfun,beta0);
        
        fprintf(rid, '%s against %s\n', astName{:}, idxName{:});
        %fprintf(rid, mdl);
    end  
end

fclose(rid);

