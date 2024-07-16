# BBB [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Bureau for Business Bean (BBB) group

        # Members:
        Kaelen 
        Michael
        Phoenix 
        Fruzsi

  ## <span id=Description> Description </span>
  A sales forecast application

  ## Elevator Pitch 
  [For]
  Super cafe branch
  [Who]
  Needs a data pipeline automation software for sales analysis and forecasting
  [The]
  Bean Business Bureau data system© 
  [Is a]
  Analysis and visualization tool for business planning & forecasting
  [That]
  Tracks key metrics such as overall sales & product popularity in various time frames
  [Unlike]
  How is this different to competition filtered data for bespoke graphs & visualizations
  easy to add data with CSV - column naming & error detection
  [Our product]
  Accurate, reliable, durable, secure - cleansing, Expandable, intuitive, dynamic

  ## Contents
  -[Description](#Description)  
  -[Install](#Install)  
  -[Usage Info](#Usage)  
  -[Contribution](#Contribution)  
  -[Questions](#Questions)  
  -[Tests](#Tests)  
  -[License](#License)  

  ## Product initiation document
  https://docs.google.com/document/d/1FSQwxu9fgONe1-Cq1r67GGJAH0eON9phLxYBTDiPlAs/edit?usp=sharing

  ## Group board
  https://miro.com/app/board/uXjVK5mj_K8=/

  ## <span id=Install> Install </span>
  1. Clone this repo in terminal using ***git clone https://github.com/generation-de-nat2/Bureau-for-Bean-Business.git*** or by simply downloading it as a zip file
  2. Make sure you have a working version of AWS CLI and have setup an SSO profile. For instructions and more info see: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html
  3. #Leave the rest for later 
  aws cloudformation deploy --template-file bbb-stack-template-S3.yml --stack-name bbb-stack --region eu-west-1 --profile test
  see requirements.txt

  ## <span id=Usage> Usage </span>
  run remove_colums_import CSV.py

  ## <span id=Contribution> Contribution </span>
  Created by BBBgroup  
  See github to contribute or report bugs: https://github.com/https://github.com/generation-de-nat2/Bureau-for-Bean-Business

  ## <span id=Questions> Questions </span>
  For issues or feature requests: https://github.com/https://github.com/generation-de-nat2/Bureau-for-Bean-Business  
  For other questions, please email me: 

  ## <span id=Tests> Tests </span>
  formal tests to come

  ## <span id=License> License </span>
  MIT  
  https://opensource.org/licenses/MIT  
  Copyright BBBgroup
      Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:  
      
      The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
      
      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  
