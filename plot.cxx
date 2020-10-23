{
TCanvas * c1 = new TCanvas("c1");
ifstream ifs("test_random.txt");
//ifstream ifs("test.txt");

double a,b,c,d;
vector<double> step;
vector<double> y_row;
vector<double> y_kalman;
vector<double> gain;
while(ifs>>a>>b>>c>>d){
				step.push_back(a);
				y_row.push_back(b);
				y_kalman.push_back(c);
				gain.push_back(d);
}

TGraph *g1 = new TGraph(step.size(),&step[0],&y_row[0]);
g1->SetTitle("Temp");
g1->GetXaxis()->SetTitle("number");
g1->GetYaxis()->SetTitle("Temperature");
g1->Draw();

TGraph *g2 = new TGraph(step.size(),&step[0],&y_kalman[0]);
g2->SetLineColor(2);
g2->Draw("SAME");

TGraph *g3 = new TGraph(step.size(),&step[0],&gain[0]);
g3->SetLineColor(kGreen+2);
g3->Draw("SAME");

TLegend *l= new TLegend(0.7,0.7,0.9,0.9,"temp-comparison");
l->AddEntry(g1,"raw_temp","l");
l->AddEntry(g2,"kalman_temp","l");
l->AddEntry(g3,"10average_temp","l");
l->Draw();
}
