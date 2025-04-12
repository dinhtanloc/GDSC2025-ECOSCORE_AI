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
                Most investors in Vietnam lack the foundational knowledge needed to enter the stock market. As a result, they often rely on trusted sources and seek superficial information on platforms like Chat GPT. EXcore AI is designed to be a reliable advisor with extensive training in financial and stock market knowledge. It not only answers financial queries effectively but also pulls data directly from the Vnstock exchange, offering up-to-date and accurate information. Additionally, EXcore AI provides a practical environment for data scientists to test their models with the latest stock data, enhancing their research and experience.
                </p>

                <p className="section__description">
                <br/>
                In Vietnam, many investors lack the foundational knowledge needed to confidently enter the stock market. As a result, they often rely on established sources and seek out basic information from platforms like Chat GPT. Recognizing this gap, EXcore AI has been developed to serve as a trusted advisor with a vast amount of financial and stock market knowledge.
                EXcore AI stands out by offering accurate and up-to-date information, thanks to its ability to pull data directly from the Vnstock exchange. This real-time data integration distinguishes EXcore AI from other chatbot platforms, ensuring that users receive the most current and precise information available.
                Moreover, EXcore AI goes beyond merely providing information. It also offers a practical environment for data scientists to test and validate their models using the latest stock data. This feature not only supports research and development but also enhances the overall user experience by providing a hands-on tool for financial analysis and experimentation. ed in the stock market.
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