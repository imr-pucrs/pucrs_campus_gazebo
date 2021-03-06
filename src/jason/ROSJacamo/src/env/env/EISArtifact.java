package env;

import jason.JasonException;
import jason.asSyntax.*;
import rosTest.RosInterface;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.logging.Logger;

import cartago.AgentId;
import cartago.Artifact;
import cartago.INTERNAL_OPERATION;

public class EISArtifact extends Artifact implements AgentListener {

	private Logger logger = Logger.getLogger(EISArtifact.class.getName());

	private Map<String, AgentId> agentIds;
	private Map<String, String> agentToEntity;
	private List<Literal> start = new ArrayList<Literal>();
	private List<Literal> percs = new ArrayList<Literal>();
	private List<Literal> signalList = new ArrayList<Literal>();

	private List<String> previousList = new ArrayList<String>();
	
	private static Set<String> agents = new ConcurrentSkipListSet<String>();

	private RosInterface ri = null;
	private boolean receiving;
	private int lastStep = -1;
	private int round = 0;

	
	public EISArtifact() {
		agentIds      = new ConcurrentHashMap<String, AgentId>();
		agentToEntity = new ConcurrentHashMap<String, String>();		
	}
	
	protected void init(String config) throws IOException, InterruptedException {
		ri = new RosInterface(config);
        try {
            ri.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        ri.attachAgentListener(this);
        
        receiving = true;
        execInternalOp("receiving", "ag1");
	}
	
	public static Set<String> getRegisteredAgents(){
		return agents;
	}
	

	

	@INTERNAL_OPERATION
	void receiving(String agent) throws JasonException {
		lastStep = -1;
		Collection<Percept> previousPercepts = new ArrayList<Percept>();
		while(!ri.isEntityConnected(agent))
			await_time(100);
		while (receiving) {
			await_time(500);
			if (ri != null) {
				try {
					Collection<Percept> percepts = ri.getNextPerception(agent,agent);
					
					if (!percepts.isEmpty()) {
							updatePerception(previousPercepts, percepts);
							previousPercepts = percepts;
						}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
	}	
	
	

	
	private void updatePerception(Collection<Percept> previousPercepts, Collection<Percept> percepts) throws JasonException {
		// compute new perception
		String agent = "ag1";
		Literal step 				= null;
		List<Literal> auction 		= new ArrayList<Literal>();
		Literal lastActionResult 	= null;
		Literal actionID 			= null;
		
		for (Percept old: previousPercepts) {
			if (previousList.contains(old.getName())) { // not perceived anymore	
					Literal literal = Translator.perceptToLiteral(old);
					try{
						//System.out.println("Removing belief:"+old.getName());
						previousList.remove(old.getName());
						removeObsPropertyByTemplate(old.getName(), (Object[]) literal.getTermsArray());
					}
					catch (Exception e) {
						logger.info("error removing old perception "+literal+" "+e.getMessage());
						logger.info("P*** "+percepts);
						logger.info("O*** "+previousPercepts);
					}
			}
		}
		
		for (Percept percept: percepts) {
			Literal literal = Translator.perceptToLiteral(percept);
				//System.out.println("Defining belief:"+percept.getName());
				previousList.add(percept.getName());
				defineObsProperty(percept.getName(), (Object[]) literal.getTermsArray());
		}

				
	}	
	
	
    //@Override
    public void handlePercept(String agent, Percept percept) {}

	public void handlePercept(String arg0, eis.iilang.Percept arg1) {
		// TODO Auto-generated method stub
		
	}
   
}

