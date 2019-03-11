df <- read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')
df <- as.data.frame(df)

ui <- fluidPage(
  headerPanel('Death Rates by Various Cause for each State'),
  sidebarPanel(
    selectInput('disease', 'Disease', unique(df$ICD.Chapter), selected='Certain conditions originating in the perinatal period'),
    selectInput('year', 'Year', unique(df$Year), selected='2010')
  ),
  mainPanel(
    plotOutput('plot1')
  )
)

server <- shinyServer(function(input, output, session) {
  
  selectedData <- reactive({
    dfSlice <- df %>%
      filter(ICD.Chapter == input$disease, Year == input$year)
  })
  
  output$plot1 <- renderPlot({
    
    dfSlice <- df %>%
      filter(ICD.Chapter == input$disease, Year == input$year)
    dfSlice <- as.data.frame(dfSlice)
    
    ggplot(selectedData(), aes(x = State, y = Crude.Rate)) +
      geom_bar(stat = 'identity') +
      geom_hline(yintercept=mean(dfSlice$Crude.Rate), linetype="dashed", color = "red", show.legend = TRUE) + 
      geom_hline(yintercept=median(dfSlice$Crude.Rate), linetype="dashed", color = "blue", show.legend = TRUE) +
      labs(caption = "Blue line reflects national average. Red line reflects national median.")
  })
  
  
})
shinyApp(ui = ui, server = server)