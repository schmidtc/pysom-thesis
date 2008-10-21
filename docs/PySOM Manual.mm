<map version="0.8.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1223248477773" ID="Freemind_Link_376679635" MODIFIED="1223248881518" TEXT="PySOM Manual">
<node CREATED="1223248884252" FOLDED="true" ID="Freemind_Link_528587726" MODIFIED="1223249800001" POSITION="right" TEXT="Intro">
<edge WIDTH="thin"/>
<node CREATED="1223249163125" ID="Freemind_Link_707954679" MODIFIED="1223249219858" TEXT="PySOM is an implementation of the Self-Organizing Map training algorithm written in the Python Programming Language."/>
<node CREATED="1223249220495" ID="Freemind_Link_1632558200" MODIFIED="1223249291698" TEXT="What makes PySOM unique from other implementations is that the network topology is not hard wired, instead we represent the topology as a graph."/>
<node CREATED="1223249292367" ID="Freemind_Link_1042004081" MODIFIED="1223249346035" TEXT="The NetworkX python library is used to manage the graph."/>
<node CREATED="1223249365960" ID="Freemind_Link_1081351783" MODIFIED="1223249427528" TEXT="This document is intended to provide an overview of PySOM and help users get started with training their SOMs."/>
<node CREATED="1223249428220" ID="Freemind_Link_1927767488" MODIFIED="1223249470470" TEXT="In it&apos;s current form some basic knowledge of the Python Programming language is required to use PySOM"/>
<node CREATED="1223249472019" ID="Freemind_Link_1018626559" MODIFIED="1223249512818" TEXT="I hope to provide a more robust graphical user interface in the future, but for now PySOM can only be accessed programmitcally."/>
<node CREATED="1223249534753" ID="Freemind_Link_240614022" MODIFIED="1223249665901" TEXT="In the following sections you will learn how to setup your topology, organize your data, set your training paramenters, and train your SOM."/>
<node CREATED="1223249666674" ID="Freemind_Link_807120523" MODIFIED="1223249729292" TEXT="Some useful functions and instructions for visualizing your SOM will also be provided, but most if this will need to be down without the help of PySOM."/>
<node CREATED="1223249809685" ID="Freemind_Link_46774827" MODIFIED="1223249820222" TEXT="Library Organiztion">
<node CREATED="1223249820802" ID="Freemind_Link_1009790772" MODIFIED="1223249824679" TEXT="som.py">
<node CREATED="1223249825732" ID="Freemind_Link_567368777" MODIFIED="1223249839213" TEXT="Contains the training code"/>
</node>
</node>
<node CREATED="1223248886165" ID="Freemind_Link_1664257889" MODIFIED="1223248888873" TEXT="Topology">
<node CREATED="1223249005146" ID="Freemind_Link_672716319" MODIFIED="1223249092114" TEXT="Any valid undirected NetworkX can be used as the topology for your SOM.  The nodes of the graph will be treated as neurons."/>
<node CREATED="1223249133233" ID="Freemind_Link_957442368" MODIFIED="1223249153277" TEXT="Several utility function are provided to help creat your graphs."/>
</node>
<node CREATED="1223248895033" ID="Freemind_Link_1624614560" MODIFIED="1223248896149" TEXT="Data"/>
<node CREATED="1223248897113" ID="Freemind_Link_850087041" MODIFIED="1223248899870" TEXT="Training"/>
<node CREATED="1223248900275" ID="Freemind_Link_989431844" MODIFIED="1223248902503" TEXT="Visualize"/>
</node>
<node CREATED="1223250006181" FOLDED="true" ID="Freemind_Link_1467846724" MODIFIED="1223250012067" POSITION="right" TEXT="Installation">
<node CREATED="1223251103094" FOLDED="true" ID="Freemind_Link_1493726936" MODIFIED="1223251107555" TEXT="Requirements">
<node CREATED="1223250012511" ID="Freemind_Link_74409514" MODIFIED="1223250179919" TEXT="PySOM requires a Python Version 2.4 or later.  Major version releases of Python (eg. from 2.0 to 3.0) are not backwards compatible and PySOM should not be expected to work with future major releases."/>
<node CREATED="1223250216700" ID="Freemind_Link_1298461132" MODIFIED="1223250254785" TEXT="In addition the following Python Libraries are required."/>
<node CREATED="1223250255317" ID="Freemind_Link_1877183237" MODIFIED="1223250276058" TEXT="Version numbers used for development are provided, but future version are expected to work."/>
<node CREATED="1223250277055" ID="Freemind_Link_392554020" MODIFIED="1223250390495" TEXT="Numpy (1.0.4)"/>
<node CREATED="1223250391100" ID="Freemind_Link_497056518" MODIFIED="1223250440046" TEXT="NetworkX (0.35.1)"/>
<node CREATED="1223250475451" ID="Freemind_Link_202757107" MODIFIED="1223250567729" TEXT="To create spherical topologies you also need the STRI_PACK and SXYZ_VORONOI software packages, these require a fortran complier."/>
<node CREATED="1223250520488" ID="Freemind_Link_1350416118" MODIFIED="1223250618353" TEXT="To create Geoesic topologies you will need the Dome software package."/>
<node CREATED="1223250975559" ID="Freemind_Link_1069689905" MODIFIED="1223251005681" TEXT="To visualize the SOM you will need ESRI&apos;s ArcMap or another method for creating ShapeFiles."/>
</node>
<node CREATED="1223251123926" ID="Freemind_Link_266649466" MODIFIED="1223251127963" TEXT="PySOM">
<node CREATED="1223251128376" ID="Freemind_Link_891219149" MODIFIED="1223251169884" TEXT="You can download PySOM from http://code.google.com/p/pysom-thesis/downloads/list"/>
</node>
</node>
<node CREATED="1223248537803" FOLDED="true" ID="Freemind_Link_1668628714" MODIFIED="1223248541008" POSITION="right" TEXT="Topology">
<node CREATED="1223248541468" FOLDED="true" ID="Freemind_Link_1548700446" MODIFIED="1223248546266" TEXT="Intro">
<node CREATED="1223248546622" ID="Freemind_Link_190729873" MODIFIED="1223248559911" TEXT="NetworkX Undirected Graph"/>
</node>
<node CREATED="1223248560420" ID="Freemind_Link_1797713024" MODIFIED="1223248567211" TEXT="Rectangular"/>
<node CREATED="1223248567551" ID="Freemind_Link_320481220" MODIFIED="1223248569043" TEXT="Hexagon"/>
<node CREATED="1223248569512" ID="Freemind_Link_1777152345" MODIFIED="1223248572236" TEXT="Geodesic">
<node CREATED="1223248572698" ID="Freemind_Link_658639264" MODIFIED="1223248574741" TEXT="Dome"/>
<node CREATED="1223248575522" ID="Freemind_Link_861421812" MODIFIED="1223248586170" TEXT="stri_pack"/>
<node CREATED="1223248607159" ID="Freemind_Link_1552151459" MODIFIED="1223248813849" TEXT="parseDelaunay"/>
</node>
<node CREATED="1223248589472" ID="Freemind_Link_118548096" MODIFIED="1223248593645" TEXT="Spherical">
<node CREATED="1223248594002" ID="Freemind_Link_1140750880" MODIFIED="1223248599840" TEXT="Rahkmonv"/>
<node CREATED="1223248600276" ID="Freemind_Link_258741083" MODIFIED="1223248604306" TEXT="stri_pack"/>
<node CREATED="1223248607159" ID="Freemind_Link_248931813" MODIFIED="1223248815618" TEXT="parseDelaunay"/>
</node>
</node>
<node CREATED="1223248483234" FOLDED="true" ID="_" MODIFIED="1223248488130" POSITION="right" TEXT="Data">
<node CREATED="1223248488551" FOLDED="true" ID="Freemind_Link_1566643953" MODIFIED="1223248491316" TEXT="FileFormat">
<node CREATED="1223248491688" ID="Freemind_Link_1509298993" MODIFIED="1223248494605" TEXT="Dims"/>
<node CREATED="1223248495322" ID="Freemind_Link_1515876548" MODIFIED="1223248497662" TEXT="Obs"/>
<node CREATED="1223248498307" ID="Freemind_Link_1185905145" MODIFIED="1223248498927" TEXT="Obs"/>
<node CREATED="1223248499555" ID="Freemind_Link_1358739651" MODIFIED="1223248500175" TEXT="Obs"/>
<node CREATED="1223248501669" ID="Freemind_Link_854918841" MODIFIED="1223248502512" TEXT="...."/>
</node>
<node CREATED="1223248504725" FOLDED="true" ID="Freemind_Link_1294154974" MODIFIED="1223248508739" TEXT="ObsFile">
<node CREATED="1223248513483" ID="Freemind_Link_844419491" MODIFIED="1223248515901" TEXT="Complete"/>
<node CREATED="1223248516218" ID="Freemind_Link_649325600" MODIFIED="1223248520495" TEXT="Sparse"/>
</node>
</node>
<node CREATED="1223248648048" FOLDED="true" ID="Freemind_Link_1116637899" MODIFIED="1223248652214" POSITION="right" TEXT="Training">
<node CREATED="1223248652690" ID="Freemind_Link_102920195" MODIFIED="1223248655943" TEXT="Parameters">
<node CREATED="1223248656484" ID="Freemind_Link_1126678743" MODIFIED="1223248661345" TEXT="Dims"/>
<node CREATED="1223248661654" ID="Freemind_Link_710784641" MODIFIED="1223248665403" TEXT="maxN"/>
<node CREATED="1223248671826" ID="Freemind_Link_1126978143" MODIFIED="1223248673806" TEXT="tSteps"/>
<node CREATED="1223248676420" ID="Freemind_Link_1343956724" MODIFIED="1223248678248" TEXT="alpha0"/>
</node>
<node CREATED="1223248684679" ID="Freemind_Link_336703420" MODIFIED="1223248688668" TEXT="Phase I"/>
<node CREATED="1223248688993" ID="Freemind_Link_1106654167" MODIFIED="1223248690645" TEXT="Phase II"/>
</node>
<node CREATED="1223248759767" ID="Freemind_Link_127807964" MODIFIED="1223248762979" POSITION="right" TEXT="Saving"/>
<node CREATED="1223248763472" ID="Freemind_Link_1325218999" MODIFIED="1223248765285" POSITION="right" TEXT="Loading"/>
<node CREATED="1223248767626" ID="Freemind_Link_238774452" MODIFIED="1223248769206" POSITION="right" TEXT="Mapping"/>
<node CREATED="1223593950993" FOLDED="true" ID="Freemind_Link_1276918422" MODIFIED="1223594037732" POSITION="right" TEXT="API Examples">
<node CREATED="1223593952972" FOLDED="true" ID="Freemind_Link_985048586" MODIFIED="1223594160893" TEXT="hex">
<node CREATED="1223594067400" ID="Freemind_Link_542053762" MODIFIED="1223594172067" TEXT="import pysom"/>
<node CREATED="1223594199246" ID="Freemind_Link_1384719524" MODIFIED="1223594211144" TEXT="from pysom.utils import hex"/>
<node CREATED="1223594380001" ID="Freemind_Link_726382309" MODIFIED="1223594469605" TEXT="# Create a Hexagonal Graph"/>
<node CREATED="1223594228589" ID="Freemind_Link_888454498" MODIFIED="1223594234348" TEXT="rows = 20"/>
<node CREATED="1223594234977" ID="Freemind_Link_209278698" MODIFIED="1223594238927" TEXT="cols = 20"/>
<node CREATED="1223594172776" ID="Freemind_Link_1739243240" MODIFIED="1223594321621" TEXT="hex_20_20 = hex.hexGraph(rows,cols)"/>
<node CREATED="1223594503212" ID="Freemind_Link_777214119" MODIFIED="1223594503212" TEXT=""/>
<node CREATED="1223594505269" ID="Freemind_Link_1533755716" MODIFIED="1223594516015" TEXT="# Initialize the SOM object"/>
<node CREATED="1223594279892" ID="Freemind_Link_247568877" MODIFIED="1223594748466" TEXT="S = pysom.som.GraphTopology(G=hex_20_20,type=&apos;hex&apos;)"/>
<node CREATED="1223594372620" ID="Freemind_Link_126896522" MODIFIED="1223594528685" TEXT="# Set the training Parameters"/>
<node CREATED="1223594529226" ID="Freemind_Link_1597641828" MODIFIED="1223594702953" TEXT="S.dims = 3 #The number of dimmensions in the training data"/>
<node CREATED="1223594577131" ID="Freemind_Link_299803622" MODIFIED="1223594701160" TEXT="S.maxN = 0.5 #The percent of the network to include in the first training step"/>
<node CREATED="1223594636715" ID="Freemind_Link_24394497" MODIFIED="1223594699575" TEXT="S.tSteps = 100000 #The number training steps to perform"/>
<node CREATED="1223594674575" ID="Freemind_Link_24134948" MODIFIED="1223594697198" TEXT="S.alpha0 = 0.04 #The initial learning rate"/>
<node CREATED="1223594817451" ID="Freemind_Link_468515733" MODIFIED="1223594817451" TEXT=""/>
<node CREATED="1223594833443" ID="Freemind_Link_1188367247" MODIFIED="1223594853209" TEXT="#Randomly Initialize the reference vectors."/>
<node CREATED="1223594819956" ID="Freemind_Link_1955551091" MODIFIED="1223594832582" TEXT="S.randInit()"/>
<node CREATED="1223594705801" ID="Freemind_Link_594176681" MODIFIED="1223594705801" TEXT=""/>
<node CREATED="1223594712923" ID="Freemind_Link_516159158" MODIFIED="1223594721732" TEXT="#Setup the observation File"/>
<node CREATED="1223594722800" ID="Freemind_Link_480649389" MODIFIED="1223594798164" TEXT="f = pysom.data.ObsFile(&apos;examples/training_data/states.dat&apos;,&apos;complete&apos;)"/>
<node CREATED="1223594860482" ID="Freemind_Link_1083350414" MODIFIED="1223594860482" TEXT=""/>
<node CREATED="1223594863475" ID="Freemind_Link_486058959" MODIFIED="1223594881904" TEXT="# Save the initial State (optional)"/>
<node CREATED="1223594882997" ID="Freemind_Link_1935928158" MODIFIED="1223594960281" TEXT="S.save(&quot;examples/output/&quot;, &quot;initial_state&quot;)"/>
<node CREATED="1223594961087" ID="Freemind_Link_1571864304" MODIFIED="1223594961087" TEXT=""/>
<node CREATED="1223594966514" ID="Freemind_Link_1518426859" MODIFIED="1223594981341" TEXT="#Train the som"/>
<node CREATED="1223594987077" ID="Freemind_Link_1851023221" MODIFIED="1223594992298" TEXT="S.run(f)"/>
<node CREATED="1223594994224" ID="Freemind_Link_833231312" MODIFIED="1223595008355" TEXT="#Map the observation onto the SOM (optional)"/>
<node CREATED="1223595009064" ID="Freemind_Link_1944609917" MODIFIED="1223595011821" TEXT="S.map()"/>
<node CREATED="1223595012602" ID="Freemind_Link_1883364724" MODIFIED="1223595027133" TEXT="#Save the trained SOM and the Map"/>
<node CREATED="1223595027690" ID="Freemind_Link_467972896" MODIFIED="1223595062384" TEXT="S.save(&quot;examples/output/&quot;,&quot;phase1&quot;)"/>
<node CREATED="1223595062957" ID="Freemind_Link_115712894" MODIFIED="1223595062957" TEXT=""/>
<node CREATED="1223595065430" ID="Freemind_Link_1192943279" MODIFIED="1223595078481" TEXT="#Adjust training parameters for phase Two training,"/>
<node CREATED="1223595079230" ID="Freemind_Link_180307719" MODIFIED="1223595098021" TEXT="S.maxN = 0.333"/>
<node CREATED="1223595102170" ID="Freemind_Link_358640538" MODIFIED="1223595112218" TEXT="S.tSteps = 1000000"/>
<node CREATED="1223595113696" ID="Freemind_Link_615915644" MODIFIED="1223595128251" TEXT="S.alpha0 = 0.03"/>
<node CREATED="1223595185102" ID="Freemind_Link_456019148" MODIFIED="1223595185102" TEXT=""/>
<node CREATED="1223595186182" ID="Freemind_Link_1645400975" MODIFIED="1223595210527" TEXT="#Reset the observation file"/>
<node CREATED="1223595179915" ID="Freemind_Link_1414197737" MODIFIED="1223595183969" TEXT="f.reset()"/>
<node CREATED="1223595240947" ID="Freemind_Link_586363882" MODIFIED="1223595247306" TEXT="#Start training"/>
<node CREATED="1223595248319" ID="Freemind_Link_1838120582" MODIFIED="1223595251989" TEXT="S.run()"/>
<node CREATED="1223595252481" ID="Freemind_Link_49475480" MODIFIED="1223595254118" TEXT="#Save"/>
</node>
</node>
</node>
</map>
