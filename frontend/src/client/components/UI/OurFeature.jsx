import RadarChart from "@client/components/UI/RadarChart"
import { Container, Row, Col } from "reactstrap";

const OurFeature = ()=>{
    return(
        <section className="about__page-section" style={{backgroundColor:'#f7fbf1'}}>
        <Container>
          <Row>
            <Col lg="6" md="6" sm="12">
              <div className="about__page-img">
                {/* <img src={driveImg} alt="" className="w-100 rounded-3" /> */}
                <RadarChart/>;
              </div>
            </Col>

            <Col lg="6" md="6" sm="12">
              <div className="about__page-content">
                <h2 className="section__title">
                EXcore AI: Vietnam's first ESG Rating Platform with a chatbot for better user experience.
                </h2>

                <p className="section__description">
                Most businesses in Vietnam, especially small and medium-sized enterprises (SMEs), face significant challenges in independently creating comprehensive ESG reports. At the same time, larger corporations invest substantial effort in this process due to the lack of technological integration, making it inefficient and resource-intensive. Similarly, most investors in Vietnam lack the foundational knowledge necessary to participate effectively in the stock market. Consequently, they often depend on trusted sources or superficial information obtained from platforms like Chat GPT.
                </p>

                <p className="section__description">
                <br/>
                EXcore AI addresses these gaps by serving as a reliable advisor with extensive training in financial and stock market expertise. It not only provides accurate answers to financial queries but also directly accesses real-time data from the Vnstock exchange, ensuring users receive up-to-date and precise information. Moreover, EXcore AI offers a practical platform for data scientists to test their models using the latest stock market data, thereby enriching their research capabilities and enhancing their overall experience.
                </p>

                <div className=" d-flex align-items-center gap-3 mt-4">
                  <span className="fs-4">
                    <i className="ri-phone-line"></i>
                  </span>

                  {/* <div>
                    <h6 className="section__subtitle">Need Any Help?</h6>
                    <h4>+0938922810</h4>
                  </div> */}
                </div>
              </div>
            </Col>
          </Row>
        </Container>
      </section>
    );
};
export default OurFeature;