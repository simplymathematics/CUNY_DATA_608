library(ggplot2)
library(dplyr)
library(shiny)
df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')
df <- as.data.frame(df)
df$YoY <- NULL
dim(df)
diseases = unique(df$ICD.Chapter)
years = 1999:2010

national <- data.frame(
  National.Mean = numeric(),
  ICD.Chapter = factor(),
  Year = integer(),
  Deaths = integer(),
  Population = integer(),
  Crude.Rate = numeric()
)
for (i in 1:length(years)){
  for(j in 1:length(diseases)){
    slice <- filter(df, ICD.Chapter == diseases[j] & Year == years[i])
    if(years[i] == 1999){
      last.slice <- slice
    }
    else{
      last.slice <- filter(df, ICD.Chapter == diseases[j] & Year == years[i - 1])
    }
    last.slice$Old.Rate <- last.slice$Crude.Rate
    last.slice$Year <- last.slice$Year+1
    last.slice$Crude.Rate <- NULL
    last.slice$Deaths <- NULL
    
    big <- merge(slice, last.slice, by = c("ICD.Chapter", "Year", "State"), all = TRUE)
    big$Population.y <- NULL
    big$Old.Rate <- (big$Crude.Rate - big$Old.Rate)
    colnames(big) <- c("ICD.Chapter", "Year", "State", "Deaths", "Population", "YoY")
    national.mean <- mean(big$YoY, na.rm =TRUE)
    tmp <- merge(df, big, all = TRUE)
    tmp[,7] <- NULL
    tmp[,7] <- NULL
    
  }
  
}

cleaned <- filter(tmp, Year != 1999)

ui <- fluidPage(
  headerPanel('Death Rates by Various Cause for each State'),
  sidebarPanel(
    selectInput('disease', 'Disease', unique(cleaned$ICD.Chapter), selected='Certain conditions originating in the perinatal period')
  ),
  mainPanel(
    plotOutput('plot1')
  )
)

server <- shinyServer(function(input, output) {
  
  selectedData <- reactive({
    dfSlice <- cleaned %>%
      filter(ICD.Chapter == input$disease, Year == '2010')
    
    dfSlice <- as.data.frame(dfSlice)
    
    
  })
  
  output$plot1 <- renderPlot({
    
    dfSlice <- cleaned %>%
      filter(ICD.Chapter == input$disease, Year == '2010')
    dfSlice <- as.data.frame(dfSlice)
    
    ggplot(selectedData(), aes(x = State, y = Crude.Rate)) +
      geom_col(stat = 'identity', binwidth = .5)+
      geom_hline(yintercept=mean(dfSlice$Crude.Rate), linetype="dashed", color = "red", show.legend = TRUE) + 
      geom_hline(yintercept=median(dfSlice$Crude.Rate), linetype="dashed", color = "blue", show.legend = TRUE) +
      labs(caption = "Blue line reflects national average. Red line reflects national median.") + 
      ylab("YoY % Change" )+
      xlab("State") + 
      theme(panel.background = element_blank(), 
            axis.text = element_text(size = 10)
            ) +
      coord_flip()
      
    
  })
  
})

shinyApp(ui = ui, server = server)