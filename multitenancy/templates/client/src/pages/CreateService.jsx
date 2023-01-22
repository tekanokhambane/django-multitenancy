import { useEffect, useRef, useState } from "react";
import axios from "axios";


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


const CreateService = () => {
	const [plans, setPlans] = useState([]);
	const [selectPlan, setSelectPlan] = useState();
	const [planPrice, setPlanPrice] = useState();
	const [planName, setplanName] = useState();
	const [annualPrice, setAnnualPrice] = useState();
	const [weeklyPrice, setWeeklyPrice] = useState();
	const [quartlyPrice, setQuartlyPrice] = useState();
	const [duration, setDuration] = useState("monthly");
	const isLoading = useRef(true);

	const handleChange = (event) => {
		setDuration(event.target.value);
	};

	const handleClick = (e, plan, i) => {
		console.log(plan);
		setSelectPlan(plan.id);
		setPlanPrice(plan.price);
		setAnnualPrice(plan.price_annually);
		setWeeklyPrice(plan.price_weekly);
		setQuartlyPrice(plan.price_quartely);
		setplanName(plan.name);
	};
	useEffect(() => {
		if (isLoading.current) {
			isLoading.current = false;
			let listItems = [];
			axios.get(`/api/multitenancy/plans`).then((res) => {
				listItems = [res.data];
				setPlans(...listItems);
				setSelectPlan(res.data[0].id);
				setplanName(res.data[0].name);
				setPlanPrice(res.data[0].price);
				setAnnualPrice(res.data[0].price_annually);
				setWeeklyPrice(res.data[0].price_weekly);
				setQuartlyPrice(res.data[0].price_quartely);
			});
		}
	}, []);

	const createService = (e) => {
		e.preventDefault();
		let data = {
			subscription_duration: duration,
			plan:selectPlan
		}

		let headers= {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		}
		
		const request = new Request(
			`/api/multitenancy/plans/create`,
			{
				method: 'POST',
				headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
			},
				//mode:'same-origin',
				body:JSON.stringify(data)
			}
			);
			fetch(request).then((resp)=>resp.json()).then((response)=>{
				console.log(response)
			  
			}).catch((error)=>{
			console.log(error)
			})
		  
		  
		
		// axios.post(`/api/multitenancy/plans/create`, data, headers)
		// 	.then((response) => {
		// 	console.log(response)
		// 	}).catch((error) => {
		// 	console.log(error)
		// })
	};

	return (
		<section
			className="content"
			style={{ paddingBottom: "100px", height: "100%" }}
		>
			<div className="container-fluid">
				<div className="row">
					<div className="col text-muted text-center">
						<button type="button" className="btn btn-info btn-lg">
							Launch Service
						</button>
						<h2 className="text-dark">Create a service</h2>
						<p className="p-5">
							Choose a plan below to take advantage of a full account
							immediately! Your account will be billed at the start of your next
							billing cycle.
						</p>
					</div>
				</div>
				<div class="row">
					<div class="service-list">
						{plans.map((plan, i) => (
							<div
								key={plan.id}
								className={`service-card ${
									selectPlan == plan.id ? "border-success" : ""
								}`}
								onClick={(e) => handleClick(e, plan, i)}
							>
								<div
									class={`service-card-head  ${
										selectPlan == plan.id ? "bg-success" : "bg-info"
									}`}
								>
									<h3>{plan.name}</h3>
									<div class="price">
										<h4>${plan.price}</h4>
									</div>
								</div>
								<div class="service-card-body">
									<p
										class={`${
											selectPlan == plan.id ? "text-success" : "text-info"
										} `}
									>
										{plan.description}
									</p>
									{plan.features.map((feature, i) => (
										<ul>
											<li>
												{" "}
												<i
													class={`fa fa-check ${
														selectPlan == plan.id ? "bg-success" : "bg-info"
													}`}
												></i>{" "}
												{feature.name}
											</li>
										</ul>
									))}
								</div>
								<div class="service-card-footer">
									<button
										type="submit"
										class={`btn ${
											selectPlan == plan.id ? "btn-success" : "btn-dark"
										}  btn-lg`}
									>
										{selectPlan == plan.id ? "Plan Selected" : "Select Plan"}
									</button>
								</div>
							</div>
						))}
					</div>
					<div className="billing-cycle">
						<h5>
							You've selected the{" "}
							<strong className="capitalize">{planName}</strong> plan
						</h5>
						<p>Please select how you would like to be billed:</p>
						<form onSubmit={createService}>
							{/* <input type="radio" id="weekly" name="billing_cycle" value="weekly"/>
						 <label for="weekly">1 week @ $ {planPrice} /mo (total of ${weeklyPrice} due today)</label><br/> */}

							<label>
								<input
									type="radio"
									checked={duration === "monthly"}
									onChange={handleChange}
									value="monthly"
								/>
								1 month @ $ {planPrice} /mo (total of ${planPrice} due today)
							</label>
							<br />

							<label>
								<input
									type="radio"
									checked={duration === "quartely"}
									onChange={handleChange}
									value="quartely"
								/>
								3 months @ $ {planPrice} /mo (total of ${quartlyPrice} due
								today)
							</label>
							<br />

							<label>
								<input
									type="radio"
									checked={duration === "annually"}
									onChange={handleChange}
									value="annually"
								/>
								1 year @ $ {planPrice} /mo (total of ${annualPrice} due today)
							</label>
							<br />

							<div className="text-center">
								<button
									type={"submit"}
									placeholder="Submit"
									className="btn btn-success btn-lg text-center"
								>
									Create Service
								</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</section>
	);
};

export default CreateService;
