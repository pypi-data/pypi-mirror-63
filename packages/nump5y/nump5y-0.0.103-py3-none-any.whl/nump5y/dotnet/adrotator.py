Ans="""

<asp:AdRotator  runat = "server" AdvertisementFile = "adfile.xml"  Target =  "_blank" />

<Advertisements>
   <Ad>
      <ImageUrl>rose1.jpg</ImageUrl>
      <NavigateUrl>http://www.1800flowers.com</NavigateUrl>
      <AlternateText>
         Order flowers, roses, gifts and more
      </AlternateText>
      <Impressions>20</Impressions>
      <Keyword>flowers</Keyword>
   </Ad>

   <Ad>
      <ImageUrl>rose2.jpg</ImageUrl>
      <NavigateUrl>http://www.babybouquets.com.au</NavigateUrl>
      <AlternateText>Order roses and flowers</AlternateText>
      <Impressions>20</Impressions>
      <Keyword>gifts</Keyword>
   </Ad>

   <Ad>
      <ImageUrl>rose3.jpg</ImageUrl>
      <NavigateUrl>http://www.flowers2moscow.com</NavigateUrl>
      <AlternateText>Send flowers to Russia</AlternateText>
      <Impressions>20</Impressions>
      <Keyword>russia</Keyword>
   </Ad>

   <Ad>
      <ImageUrl>rose4.jpg</ImageUrl>
      <NavigateUrl>http://www.edibleblooms.com</NavigateUrl>
      <AlternateText>Edible Blooms</AlternateText>
      <Impressions>20</Impressions>
      <Keyword>gifts</Keyword>
   </Ad>
</Advertisements>

<form id="form1" runat="server">
   <div>
      <asp:AdRotator ID="AdRotator1" runat="server" AdvertisementFile  ="~/ads.xml" onadcreated="AdRotator1_AdCreated" />
   </div>
</form>


"""
