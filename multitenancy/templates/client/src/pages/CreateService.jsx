import {useEffect, useRef, useState} from "react";
import axios from "axios"
const CreateService = () => {
	const [ plans, setPlans ] = useState([]);
	const [ selectPlan, setSelectPlan ] = useState()
	const [ planPrice, setPlanPrice ] = useState()
	const [ planName, setplanName ] = useState()
	const [ annualPrice, setAnnualPrice ] = useState()
	const [ weeklyPrice, setWeeklyPrice ] = useState()
	const [quartlyPrice, setQuartlyPrice] = useState()
	const isLoading = useRef(true)
	
	const handleClick = (e, plan, i) => {
		console.log(plan)
		setSelectPlan(plan.id)
		setPlanPrice(plan.price)
		setAnnualPrice(plan.price_annually)
		setWeeklyPrice(plan.price_weekly)
		setQuartlyPrice(plan.price_quartely)
		setplanName(plan.name)
	}
  useEffect(() => {
	  if (isLoading.current) {
		isLoading.current = false
      let listItems = []
		axios.get(`/api/multitenancy/plans`).then((res) => {
		  listItems = [res.data]
			setPlans(...listItems)
			setSelectPlan(res.data[ 0 ].id)
			setplanName(res.data[ 0 ].name)
			setPlanPrice(res.data[ 0 ].price)
			setAnnualPrice(res.data[ 0 ].price_annually)
			setWeeklyPrice(res.data[ 0 ].price_weekly)
			setQuartlyPrice(res.data[ 0 ].price_quartely)
        console.log(res.data)
      })
    }
  
    
  }, [])
  
	return (
		<section className="content" style={{paddingBottom:"100px", height:"100%"}}>
			<div className="container-fluid">
				<div className="row">
					<div className="col text-muted text-center">
						<button type="button" className="btn btn-info btn-lg">
							Launch Service
						</button>
						<h2 className="text-dark">Creating a service is easy</h2>
						<p>
							It looks like you’re already a DreamHost customer, so choose a
							plan below to take advantage of a full account immediately! Your
							account will be billed at the start of your next billing cycle.
						</p>
					</div>
				</div>
				<div class="row">
					<div class="service-list">
						{plans.map((plan, i) => (
							<div key={plan.id} className={`service-card ${selectPlan == plan.id?"border-success":""}`} onClick={(e)=>handleClick(e, plan, i)}>
								<div class={`service-card-head  ${selectPlan == plan.id? "bg-success":"bg-info"}`}>
									<h3>{plan.name}</h3>
									<div class="price">
										<h4>${plan.price}</h4>
									</div>
								</div>
								<div class="service-card-body">
									<p class={`${selectPlan == plan.id?"text-success":"text-info"} `}>{plan.description}</p>
									{plan.features.map((feature, i) => (
										<ul>
											<li> <i class={`fa fa-check ${selectPlan == plan.id?"bg-success":"bg-info"}`}></i> {feature.name}</li>
										</ul>											
										))}
								</div>
								<div class="service-card-footer">
									<button type="submit" class={`btn ${selectPlan == plan.id? "btn-success":"btn-dark"}  btn-lg`}>{ selectPlan == plan.id? "Plan Selected":"Select Plan" }</button>
                    			</div>
							</div>
						))}
					</div>
					<div className="billing-cycle">
						<h5>
							You've selected the <strong className="capitalize">{planName}</strong> plan
						</h5>
						<p>
							Please select how you would like to be billed:
						</p>
						<form>
						<p>Please select your favorite Web language:</p>
						{/* <input type="radio" id="weekly" name="billing_cycle" value="weekly"/>
						 <label for="weekly">1 week @ $ {planPrice} /mo (total of ${weeklyPrice} due today)</label><br/> */}
						 <input type="radio" id="monthly"  defaultChecked={true} name="billing_cycle" value="monthly"/>
						 <label for="monthly">1 month @ $ {planPrice} /mo (total of ${planPrice} due today)</label><br/>
						 <input type="radio" id="price_quartely" name="billing_cycle" value="price_quartely"/>
						 <label for="price_quartely">3 months @ $ {planPrice} /mo (total of ${quartlyPrice} due today)</label><br/>
						 <input type="radio" id="price_annually" name="billing_cycle" value="price_annually"/>
						 <label for="price_annually">1 year @ $ {planPrice} /mo (total of ${annualPrice} due today)</label><br/>
						</form>
					</div>
				</div>
			</div>
		</section>
	);
};

export default CreateService;
